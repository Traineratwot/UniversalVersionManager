import os
import sys
from os.path import join

SEP = os.path.sep

PROGRAM_PATH = join(os.environ['APPDATA'], 'UVM')
NODE_PATH = join(PROGRAM_PATH, 'node')
PHP_PATH = join(PROGRAM_PATH, 'php')
BIN_PATH = join(PROGRAM_PATH, 'current')

CACHE_PATH = join(PROGRAM_PATH, 'cache')
TO_PATH_PATH = join(PROGRAM_PATH, 'toPath.exe')
SETTINGS_FILE = join(PROGRAM_PATH, 'settings.json')
VERBOSE = 'unittest' in sys.modules.keys() or '-d' in sys.argv
