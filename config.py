import os
import sys

from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=60)

SEP = os.path.sep

PROGRAM_PATH = os.environ['APPDATA'] + SEP + 'UVM' + SEP
NODE_PATH = PROGRAM_PATH + 'node' + SEP
PHP_PATH = PROGRAM_PATH + 'php' + SEP
BIN_PATH = PROGRAM_PATH + 'current' + SEP
TO_PATH_PATH = PROGRAM_PATH + 'toPath.exe'
VERBOSE = 'unittest' in sys.modules.keys()
