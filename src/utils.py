import json
import os
import subprocess
from os.path import exists, join

import psutil
from download import download as d
from version_parser import Version, VersionType

from src.config import TO_PATH_PATH, SEP, VERBOSE, BIN_PATH


# import re


def download(url, filename, kind="file"):
    return d(url, filename, progressbar=True, replace=False, kind=kind, verbose=VERBOSE)


def file_put_contents(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


def file_get_contents(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def addToPath(folder: str):
    os.system(f'{TO_PATH_PATH} add "{folder.rstrip(SEP)}"')
    pass


def removeToPath(folder: str):
    os.system(f'{TO_PATH_PATH} remove "{folder.rstrip(SEP)}"')
    pass


def existsToPath(folder: str):
    return os.system(f'{TO_PATH_PATH} exists "{folder.rstrip(SEP)}"') == 0
    pass


def cmd(command, verbose=False):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if verbose:
        print(result.stdout)
    return result.stdout.strip("\n").split('\n') if result.stdout else []


def createSymlink(source_dir, target_dir, verbose=VERBOSE):
    try:
        os.symlink(source_dir, target_dir)
        if verbose:
            print(f"Symlink created from {source_dir} to {target_dir}")
    except FileExistsError:
        if verbose:
            print(f"Symlink already exists at {target_dir}")
    except OSError as e:
        if verbose:
            print(f"Failed to create symlink: {e}")


def removeSymlink(target_dir, verbose=VERBOSE):
    if os.path.islink(target_dir):
        os.unlink(target_dir)
        if verbose:
            print(f"Symlink {target_dir} success delete.")
    else:
        if verbose:
            print(f"Symlink {target_dir} not exist.")


def strToVersion(string: str):
    def convert(incorrect_string: str):
        arr = incorrect_string.split('.')
        length = 3 - len(arr)
        arr = arr + ['999'] * length
        return ".".join(arr)

    try:
        v = Version(string)
        if v.get_type() != VersionType.STRIPPED_VERSION:
            string = convert(string)
    except ValueError:
        string = convert(string)
    return Version(string).__str__()


def saveUse(service, version):
    save = {}
    path = join(BIN_PATH, "current.json")
    if exists(path):
        save = json.loads(file_get_contents(path))
    save[service] = version
    file_put_contents(path, json.dumps(save))


def getUsed(service):
    save = {}
    path = join(BIN_PATH, "current.json")
    if exists(path):
        save = json.loads(file_get_contents(path))
    return save[service]


def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.name() == process_name:
            return True
    return False


def arg(version):
    class Args:
        def __init__(self):
            self.version = version

    return Args()


def namespace_to_dist(namespace):
    dist = {}
    for key, value in namespace.dict.items():
        dist[key] = value
    return dist
