from os.path import exists

from SimpleCache2.FileCache import FileCache
from SimpleCache2.MemoryCache import MemoryCache
from SimpleCache2.Settings import Settings

from src.config import CACHE_PATH, SETTINGS_FILE, PROGRAM_PATH

CACHE = FileCache(cache_dir=CACHE_PATH if exists(PROGRAM_PATH) else None)
MEMORY = MemoryCache()
SETTINGS = Settings(settings_file=SETTINGS_FILE if exists(PROGRAM_PATH) else None)
