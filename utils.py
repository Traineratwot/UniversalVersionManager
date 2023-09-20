import os
import subprocess

from download import download as d

from config import TO_PATH_PATH, SEP


def download(url, filename, kind="file"):
    return d(url, filename, progressbar=True, replace=False, kind=kind, verbose=True)


def find_max_version(input_string, versions):
    max_version = None
    for version in versions:
        if version.startswith(input_string):
            if max_version is None or version >= max_version:
                max_version = version
    return max_version


def addToPath(folder: str):
    os.system(f'{TO_PATH_PATH} add "{folder.rstrip(SEP)}"')
    pass


def removeToPath(folder: str):
    os.system(f'{TO_PATH_PATH} remove "{folder.rstrip(SEP)}"')
    pass


def existsToPath(folder: str):
    return os.system(f'{TO_PATH_PATH} exists "{folder.rstrip(SEP)}"') == 0
    pass


def cmd(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip("\n").split('\n') if result.stdout else []
