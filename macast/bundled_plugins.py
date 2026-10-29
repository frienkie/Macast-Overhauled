"""Install and update offline plugins before the plugin manager imports them."""

import hashlib
import json
import logging
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import time

logger = logging.getLogger('BundledPlugins')


def bundle_directory():
    if getattr(sys, 'frozen', False):
        resources = os.environ.get('RESOURCEPATH')
        root = Path(resources) if resources else Path(sys.executable).parent.parent / 'Resources'
    else:
        root = Path(__file__).resolve().parents[1]
    return root / 'bundled_plugins'


def version_number(value):
    return tuple(int(part) for part in re.findall(r'\d+', value))


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
            temporary = stream.name
            stream.write(data)
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            os.unlink(temporary)


def install_bundled_plugins(config_directory):
    source = bundle_directory()
    manifest_path = source / 'manifest.json'
    if not manifest_path.is_file():
        return
    config = Path(config_directory)
    state_path = config / '.bundled-plugins.json'
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        if manifest.get('schema') != 1:
            raise ValueError('Unsupported bundled plugin manifest')
        try:
            state = json.loads(state_path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            state = {}
        previous = state.get('plugins', {})
        installed = dict(previous)
        changed = []
        for plugin in manifest['plugins']:
            relative = Path(plugin['path'])
            if (len(relative.parts) != 2 or relative.parts[0] not in ('renderer', 'protocol') or
                    relative.name == '__init__.py' or relative.suffix != '.py'):
                raise ValueError('Invalid bundled plugin path')
            payload = (source / relative).read_bytes()
            digest = hashlib.sha256(payload).hexdigest()
            if digest != plugin['sha256']:
                raise ValueError('Bundled plugin checksum mismatch: {}'.format(relative))
            target = config / relative
            if target.exists():
                current = target.read_bytes()
                current_digest = hashlib.sha256(current).hexdigest()
                if current_digest == digest:
                    installed[plugin['path']] = digest
                    continue
                managed_digest = previous.get(plugin['path'])
                if managed_digest is not None and managed_digest != current_digest:
                    logger.info('Keeping customized plugin: %s', relative)
                    continue
                if managed_digest is None:
                    match = re.search(r'<macast.version>(.*?)</macast',
                                      current.decode('utf-8', errors='replace'))
                    if match is None or version_number(match.group(1)) >= version_number(plugin['version']):
                        logger.info('Keeping existing plugin: %s', relative)
                        continue
                backup = config / 'bundled-plugin-backups' / time.strftime('%Y%m%d-%H%M%S') / relative
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target, backup)
            atomic_write(target, payload)
            installed[plugin['path']] = digest
            changed.append(plugin['path'])
        updated_state = {'schema': 1, 'plugins': installed}
        if state != updated_state:
            atomic_write(state_path, (json.dumps(updated_state, indent=2) + '\n').encode('utf-8'))
        logging.getLogger('MacastLatency').info('bundled_plugins total=%d installed_or_updated=%d',
                                               len(manifest['plugins']), len(changed))
    except (OSError, ValueError, KeyError, TypeError):
        # Existing plugins remain usable if an installation cannot complete.
        logger.exception('Could not install bundled plugins')
