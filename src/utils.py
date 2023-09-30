import json
import os
import shutil
import subprocess
import sys
from os.path import exists, join

import psutil
import questionary
from download import download as d
from version_parser import Version, VersionType

from src.config import TO_PATH_PATH, SEP, VERBOSE, BIN_PATH, PROGRAM_PATH, NODE_PATH, PHP_PATH, CACHE_PATH
from src.lang import _
from src.stat import sendStat


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
    fld = folder.rstrip(SEP)
    if not existsInPath(fld):
        subprocess.run(f'{TO_PATH_PATH} add "{fld}"')
        os.system(f'set PATH=${fld};%PATH%')
        print(_('log.addedToPath', fld))
    pass


def existsInPath(folder):
    result = subprocess.run("echo %PATH%", shell=True, capture_output=True, text=True)
    return folder in result.stdout


def removeToPath(folder: str):
    fld = folder.rstrip(SEP)
    if existsInPath(fld):
        subprocess.run(f'{TO_PATH_PATH} remove "{fld}"')
        print(_('log.removeToPath', fld))
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
    if service in save:
        return save[service]
    return None


def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.name() == process_name:
            return proc.exe()
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


def isInstalled():
    return os.path.exists(PROGRAM_PATH)


def install():
    if not isInstalled():
        answer = True
        if not VERBOSE:
            q = questionary.confirm(_("ask.install", PROGRAM_PATH))
            answer = q.ask()
        if answer:
            os.makedirs(PROGRAM_PATH, exist_ok=True)
            os.makedirs(NODE_PATH, exist_ok=True)
            os.makedirs(PHP_PATH, exist_ok=True)
            os.makedirs(BIN_PATH, exist_ok=True)
            os.makedirs(CACHE_PATH, exist_ok=True)
            download(filename=TO_PATH_PATH,
                     url="https://github.com/Traineratwot/toPath/releases/download/1.2.0/toPath.exe")
            if 'uvm.exe' in sys.executable:
                shutil.copyfile(sys.executable, join(PROGRAM_PATH, "uvm.exe"))
                addToPath(PROGRAM_PATH)
            sendStat('install')
            return True
        else:
            return False
    else:
        return True
