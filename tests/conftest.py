import importlib.util
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# Windows CI for protocol/IPC logic need not compile the interface enumerator.
# Tests do not enumerate real interfaces. Native macOS builds use netifaces.
if sys.platform == 'win32' and 'netifaces' not in sys.modules and importlib.util.find_spec('netifaces') is None:
    sys.modules['netifaces'] = types.ModuleType('netifaces')
