import os

from download import download as d

from config import PROGRAM_PATH


def download(url, filename, kind="file"):
    return d(url, filename, progressbar=True, replace=False, kind=kind, verbose=True)


def find_max_version(input_string, versions):
    max_version = None
    for version in versions:
        if version.startswith(input_string):
            if max_version is None or version >= max_version:
                max_version = version
    return max_version


def addToPath(folder):
    toPath = PROGRAM_PATH + os.path.sep + 'toPath.exe'
    os.system(f'{toPath} add "{folder}"')
    pass


def removeToPath(folder):
    toPath = PROGRAM_PATH + os.path.sep + 'toPath.exe'
    os.system(f'{toPath} remove "{folder}"')
    pass


def existsToPath(folder):
    toPath = PROGRAM_PATH + os.path.sep + 'toPath.exe'
    return os.system(f'{toPath} exists "{folder}"') == 0
    pass
