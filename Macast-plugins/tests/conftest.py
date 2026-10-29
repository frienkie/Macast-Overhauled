import importlib.util
import os
import sys
import types
from pathlib import Path

core = os.environ.get('MACAST_SOURCE', str(Path(__file__).resolve().parents[2] / 'Macast'))
sys.path.insert(0, core)
if sys.platform == 'win32' and 'netifaces' not in sys.modules and importlib.util.find_spec('netifaces') is None:
    sys.modules['netifaces'] = types.ModuleType('netifaces')
