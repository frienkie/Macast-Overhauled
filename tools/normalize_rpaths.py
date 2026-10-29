"""Remove duplicate LC_RPATH entries introduced while bundling Homebrew dylibs."""

from collections import Counter
from pathlib import Path
import re
import subprocess
import sys


def rpaths(binary):
    output = subprocess.check_output(['otool', '-l', str(binary)], text=True)
    return re.findall(r'cmd LC_RPATH\s+cmdsize \d+\s+path (.*?) \(offset', output)


def normalize(root):
    for binary in [root / 'MacOS/mpv', *sorted((root / 'lib').glob('*.dylib'))]:
        duplicates = [path for path, count in Counter(rpaths(binary)).items() if count > 1]
        for path in duplicates:
            # install_name_tool can remove multiple equal entries in one call.
            while rpaths(binary).count(path) > 1:
                before = rpaths(binary).count(path)
                subprocess.run(['install_name_tool', '-delete_rpath', path, str(binary)], check=True)
                if rpaths(binary).count(path) >= before:
                    raise RuntimeError('Could not remove duplicate RPATH: ' + str(binary))
            if path not in rpaths(binary):
                subprocess.run(['install_name_tool', '-add_rpath', path, str(binary)], check=True)


if __name__ == '__main__':
    normalize(Path(sys.argv[1]))
