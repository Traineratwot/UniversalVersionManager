import math
import subprocess
from os.path import join, exists, basename
from sys import exit

import questionary
import requests
from SimpleCache2 import simple_cache
from version_parser import Version

from src.cache import CACHE, SETTINGS
from src.config import VERBOSE, PROGRAM_PATH
from src.lang import _
from src.utils import download
from version import UVM_VERSION

url = "https://api.github.com/repos/Traineratwot/UniversalVersionManager/releases/latest"


@simple_cache(CACHE, ttl=3600 * 24 * 7)
def getRelease():
    response = requests.request("GET", url)
    return response.json()


def selfUpdate():
    release = getRelease()
    current = Version(UVM_VERSION)
    latest = Version(release['tag_name'])
    if current < latest:
        skip = SETTINGS.get("skipUpdateVersion")
        if skip:
            skip = Version(skip)
            if skip >= latest:
                return
        answer = True
        file = find(release)
        size = math.floor(file['size'] / 1000000).__str__() + " Mb"
        if not VERBOSE:
            q = questionary.confirm(_("ask.newVersion", f"{release['tag_name']} ({size})", f"\n{url}\n"))
            answer = q.ask()
        if answer:
            oldFile = join(PROGRAM_PATH, "uvm.exe")
            newFile = join(PROGRAM_PATH, "uvm.exe_new")
            download(file['browser_download_url'], filename=newFile)
            if exists(newFile):
                cmd = f'cmd /c timeout /t 1 && DEL "{oldFile}" & REN "{newFile}" "{basename(oldFile)}"'
                print(cmd)
                subprocess.Popen(cmd, shell=True)
                exit(2)
            exit(1)
            pass
        else:
            SETTINGS.set("skipUpdateVersion", release['tag_name'])
        pass


def find(release):
    for asset in release['assets']:
        if 'uvm.exe' == asset['name']:
            return asset
    pass
