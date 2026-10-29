"""Prepare the sibling plugin repository as signed, offline app resources."""

import hashlib
import json
from pathlib import Path
import re
import shutil


def prepare_plugins(source, destination):
    source, destination = Path(source), Path(destination)
    entries = []
    for path in sorted(source.glob('*/*.py')):
        if path.parent.name == 'tests':
            continue
        metadata = dict(re.findall(r'<macast\.(.*?)>(.*?)</macast',
                                   path.read_text(encoding='utf-8')))
        kind = 'protocol' if 'protocol' in metadata else 'renderer' if 'renderer' in metadata else None
        if kind is None:
            continue
        target = Path(kind) / path.name
        output = destination / target
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, output)
        entries.append({
            'path': target.as_posix(),
            'title': metadata['title'],
            'version': metadata.get('version', '0'),
            'platform': metadata.get('platform', ''),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        })
        readme = path.parent / 'README.md'
        if readme.exists():
            docs = destination / 'docs' / path.parent.name
            docs.mkdir(parents=True, exist_ok=True)
            shutil.copy2(readme, docs / 'README.md')
    if not entries:
        raise RuntimeError('No plugins found in {}'.format(source))
    for name in ('LICENSE', 'README.md', 'README_ZH.md'):
        if (source / name).is_file():
            shutil.copy2(source / name, destination / name)
    (destination / 'manifest.json').write_text(
        json.dumps({'schema': 1, 'plugins': entries}, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8')
    return entries


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    source = root / 'Macast-plugins'
    if not source.is_dir():
        source = root.parent / 'Macast-plugins'
    plugins = prepare_plugins(source, root / 'bundled_plugins')
    print('Prepared {} bundled plugins'.format(len(plugins)))
