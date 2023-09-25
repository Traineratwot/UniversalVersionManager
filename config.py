import os
import sys
from os.path import join

from SimpleCache2.FileCache import FileCache

SEP = os.path.sep

PROGRAM_PATH = join(os.environ['APPDATA'], 'UVM') + SEP
NODE_PATH = join(PROGRAM_PATH, 'node') + SEP
PHP_PATH = join(PROGRAM_PATH, 'php') + SEP
BIN_PATH = join(PROGRAM_PATH, 'current') + SEP
TO_PATH_PATH = join(PROGRAM_PATH, 'toPath.exe')
VERBOSE = 'unittest' in sys.modules.keys()

CACHE = FileCache(cache_dir=join(PROGRAM_PATH, 'cache'))
