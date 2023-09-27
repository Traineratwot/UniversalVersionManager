import os
import sys
from os.path import join

from SimpleCache2.FileCache import FileCache
from SimpleCache2.LruCache import LruCache

SEP = os.path.sep

PROGRAM_PATH = join(os.environ['APPDATA'], 'UVM')
NODE_PATH = join(PROGRAM_PATH, 'node')
PHP_PATH = join(PROGRAM_PATH, 'php')
BIN_PATH = join(PROGRAM_PATH, 'current')
CACHE_PATH = join(PROGRAM_PATH, 'cache')
TO_PATH_PATH = join(PROGRAM_PATH, 'toPath.exe')
VERBOSE = 'unittest' in sys.modules.keys() or '-d' in sys.argv or '--dev' in sys.argv

CACHE = FileCache(cache_dir=CACHE_PATH)
CACHE_LRU = LruCache()
