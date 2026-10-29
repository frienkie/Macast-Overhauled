"""Prepare bilingual docs, original license records and local source for a DMG.

Run after bundling native libraries and before codesigning. Uses installed
Homebrew formulae and the metadata actually collected by py2app, without network.
"""

import argparse
from email.parser import Parser
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT if (ROOT / 'Macast-plugins').is_dir() else ROOT.parent
PLUGINS = WORKSPACE / 'Macast-plugins'
DOCS = ('README.md', 'README_ZH.md', 'BUILDING.md', 'THIRD_PARTY_NOTICES.md',
        'LICENSE', 'SOURCE-REVISIONS.json')


def copy(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def notice_file(path):
    return bool(re.match(r'^(license|licence|copying|copyright|notice|authors)([._-]|$)',
                         path.name, re.I))


def native_records(resources, output):
    cellar = Path(subprocess.check_output(['brew', '--cellar'], text=True).strip())
    mpv = Path(subprocess.check_output(['brew', '--prefix', 'mpv'], text=True).strip()).resolve()
    owners = {mpv: ['mpv']}
    for library in sorted((resources / 'bin/lib').glob('*.dylib')):
        matches = {p.resolve().parents[1] for p in cellar.glob('*/*/lib/' + library.name)}
        if len(matches) != 1:
            raise RuntimeError('Cannot identify exact native library owner: ' + library.name)
        owners.setdefault(matches.pop(), []).append(library.name)
    records = []
    for owner, files in sorted(owners.items()):
        name = owner.parent.name
        target = output / (name + '-' + owner.name)
        notices = []
        for path in owner.rglob('*'):
            relative = path.relative_to(owner)
            if path.is_file() and notice_file(path) and not any(
                    part in ('man', 'include', 'lib') for part in relative.parts[:-1]):
                copy(path, target / relative)
                notices.append(relative.as_posix())
        supplement = ROOT / 'licenses/native-supplement' / target.name
        if supplement.exists():
            shutil.copytree(supplement, target / 'upstream', dirs_exist_ok=True)
            notices.extend('upstream/' + p.relative_to(supplement).as_posix()
                           for p in supplement.rglob('*') if p.is_file())
        if not notices:
            raise RuntimeError('No native license record: ' + name)
        formula = next((owner / '.brew').glob('*.rb'))
        copy(formula, target / formula.name)
        copy(owner / 'INSTALL_RECEIPT.json', target / 'INSTALL_RECEIPT.json')
        if (owner / 'sbom.spdx.json').exists():
            copy(owner / 'sbom.spdx.json', target / 'sbom.spdx.json')
        recipe = formula.read_text()
        source = re.search(r'^  url "([^"]+)"', recipe, re.M)
        license_line = re.search(r'^  license (.+)$', recipe, re.M)
        records.append({'name': name, 'version': owner.name, 'binaries': files,
                        'upstream_source': source[1] if source else None,
                        'homebrew_license_declaration': license_line[1] if license_line else None,
                        'notices': sorted(notices)})
    return records


def python_records(resources, output):
    records = []
    with zipfile.ZipFile(resources / 'lib/python312.zip') as archive:
        for name in archive.namelist():
            if name.endswith('/'):
                continue
            path = Path(name)
            # Preserve top-level and setuptools-vendored distribution notices.
            if not any(p.endswith('.dist-info') for p in path.parts):
                continue
            if path.name not in ('METADATA', 'WHEEL') and not notice_file(path) and 'licenses' not in path.parts:
                continue
            if '..' in path.parts or path.is_absolute():
                raise ValueError(name)
            target = output / path
            target.parent.mkdir(parents=True, exist_ok=True)
            data = archive.read(name)
            target.write_bytes(data)
            if path.name == 'METADATA':
                meta = Parser().parsestr(data.decode('utf-8'))
                records.append({'name': meta['Name'], 'version': meta['Version'],
                                'metadata': name,
                                'license_expression': meta['License-Expression'],
                                'project_urls': meta.get_all('Project-URL', [])})
    python_prefix = Path(subprocess.check_output(['brew', '--prefix', 'python@3.12'], text=True).strip()).resolve()
    for path in python_prefix.glob('LICENSE*'):
        copy(path, output / 'Python-3.12' / path.name)
    if not (output / 'Python-3.12').exists():
        raise RuntimeError('Python license missing')
    return records


def source_files():
    for name in DOCS + ('使用说明.md',):
        yield WORKSPACE / name
    for name in ('Macast.py', 'setup.py', 'setup_py2app.py', 'MANIFEST.in', 'Dockerfile',
                 'README.md', 'README_ZH.md', 'LICENSE', 'build-requirements.lock.txt'):
        yield ROOT / name
    for name in ('macast', 'macast_renderer', 'mpv_ui', 'licenses', 'tools',
                 'requirements', 'tests', 'i18n', 'docs'):
        yield from (ROOT / name).rglob('*')
    yield from PLUGINS.rglob('*')


def prepare(app):
    resources = app / 'Contents/Resources'
    output = resources / 'distribution'
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)
    for name in DOCS:
        copy(WORKSPACE / name, output / name)
    for project, source in (('Macast', ROOT), ('Macast-plugins', PLUGINS)):
        copy(source / 'LICENSE', output / project / 'LICENSE')
        for path in (source / 'docs/upstream').glob('*.md'):
            copy(path, output / project / 'docs/upstream' / path.name)
    shutil.copytree(ROOT / 'mpv_ui', output / 'Macast/mpv_ui', dirs_exist_ok=True)
    shutil.copytree(ROOT / 'licenses', output / 'Macast/licenses', dirs_exist_ok=True)
    inventory = {
        'native': native_records(resources, output / 'licenses/native'),
        'python': python_records(resources, output / 'licenses/python'),
        'scope': 'Original installed license records and local source snapshot; third-party source trees are not included.',
    }
    (output / 'licenses/INVENTORY.json').write_text(json.dumps(inventory, indent=2) + '\n')
    # Distribution-only readmes use navigable links rather than source folder links.
    for name in ('README.md', 'README_ZH.md'):
        text = (output / name).read_text()
        text = text.replace('](Macast/)', '](../Macast-Local-Source.tar.gz)')
        text = text.replace('](Macast-plugins/)', '](../Macast-Local-Source.tar.gz)')
        text = text.replace('，源码分发目录中的位置为 `Macast/Macast-MacOS-v0.7-arm64.dmg`', '')
        text = text.replace(' In the source distribution, it is located at `Macast/Macast-MacOS-v0.7-arm64.dmg`.', '')
        (output / name).write_text(text)
    documentation = app.parent / 'Documentation'
    if documentation.exists():
        shutil.rmtree(documentation)
    shutil.copytree(output, documentation)
    archive = app.parent / 'Macast-Local-Source.tar.gz'
    excluded = {'__pycache__', '.pytest_cache', '.git', '.venv', '.DS_Store'}
    with tarfile.open(archive, 'w:gz') as tar:
        for path in sorted(set(source_files())):
            rel = path.relative_to(WORKSPACE)
            if path.is_file() and not excluded.intersection(rel.parts) and path.suffix not in ('.pyc', '.pyo'):
                tar.add(path, arcname='Macast-Local-Source/' + rel.as_posix(), recursive=False)
    (archive.parent / (archive.name + '.sha256')).write_text(
        hashlib.sha256(archive.read_bytes()).hexdigest() + '  ' + archive.name + '\n')
    print('Prepared {} native components and {} Python metadata records; source {} bytes'.format(
        len(inventory['native']), len(inventory['python']), archive.stat().st_size))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('app', nargs='?', type=Path, default=ROOT / 'dist/Macast.app')
    prepare(parser.parse_args().app.resolve())
