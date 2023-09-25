import json
import os
import re
import shutil
import sys

import questionary
import requests
from SimpleCache2 import simple_cache
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from version_parser import Version

from AbstractService import AbstractService
from Arguments import Arguments
from config import VERBOSE, PHP_PATH, BIN_PATH, SEP, CACHE
from utils import strToVersion, download, removeSymlink, createSymlink, saveUse, cmd, removeToPath, addToPath, getUsed

phpBaseAddress = "https://windows.php.net/downloads/releases/"


class Php(AbstractService):
    """Управление php"""

    def setup(self):
        if not os.path.exists(PHP_PATH):
            os.mkdir(PHP_PATH)
        phpBin = BIN_PATH + 'php' + SEP + 'php.exe'
        # Настройка Path
        allPhp = cmd("where php")
        if len(allPhp) > 1 or (len(allPhp) == 1 and allPhp[0] != phpBin):
            my_table = PrettyTable()
            for item in allPhp:
                my_table.add_row([item])
            answer = True
            if not VERBOSE:
                q = questionary.confirm(f"""
                Alternative installations have been found:
                {my_table}
                Do you want to replace them?
                """)
                answer = q.ask()
            if answer:
                # Интеграция с nvm
                if len(cmd("where pvm")):
                    os.system("pvm clear")
                    allPhp = cmd("where php")
                for item in allPhp:
                    if item != BIN_PATH + 'php':
                        removeToPath(os.path.dirname(item))
                    pass
                addToPath(BIN_PATH + 'php')
            else:
                exit(1)
                pass
            pass
        else:
            addToPath(BIN_PATH + 'php')
            pass

    def use(self, args: Arguments):
        if args.version:
            v = getPhpVersionFromUserRequest(args)
            path = self.path(args)
            if not os.path.exists(path):
                self.install(args)
            if not os.path.exists(path):
                return 'error'
            removeSymlink(BIN_PATH + 'php')
            createSymlink(
                target_dir=BIN_PATH + 'php',
                source_dir=path
            )
            saveUse('php', v['version'])
            return printCurrentPhpVersions()
        else:
            return printCurrentPhpVersions()
        pass
        pass

    def off(self, args: Arguments):
        pass

    def list(self, args: Arguments):
        dirs = os.scandir(PHP_PATH)
        my_table = PrettyTable()
        my_table.add_column("Version", "")
        current = getUsed('php')
        print(current)
        for dirObject in dirs:
            try:
                v = Version(dirObject.name)
                if v.__str__() == current:
                    my_table.add_row([f"({v})"])
                else:
                    my_table.add_row([v])
            except ValueError:
                pass
        return my_table
        pass

    def install(self, args: Arguments):
        v = getPhpVersionFromUserRequest(args)
        if v:
            download(filename=PHP_PATH + v['version'], url=v['link'], kind='zip')
        return 'install'
        pass

    def remove(self, args: Arguments):
        path = self.path(args)
        if path:
            answer = True
            if not VERBOSE:
                q = questionary.confirm(f"Delete this '{path}' ?")
                answer = q.ask()
            if answer:
                shutil.rmtree(path)
                return f'removed {path}'
            return 'canceled'
        return 'already removed'
        pass

    def path(self, args: Arguments):
        v = getPhpVersionFromUserRequest(args)
        if v:
            return PHP_PATH + v['version']
        pass

    def search(self, args: Arguments):
        pass


def printCurrentPhpVersions():
    php = cmd("php -v")
    return f"""{'Now used php: ' + php[0] if len(php) >= 1 else "php use error"}"""
    pass


def getPhpVersionFromUserRequest(args: Arguments):
    versions = getPhpVersions()
    version = Version(strToVersion(args.version))
    userMajor = version.get_major_version().__str__()
    userMinor = version.get_minor_version().__str__()
    userBuild = version.get_build_version().__str__()

    def find(versions_list, strict=True):
        founded = None
        if userMajor.__str__() not in versions_list:
            return None
        if userMajor in versions_list and userMinor in versions_list[userMajor] and userBuild in versions_list[userMajor][userMinor]:
            founded = {
                "version": '.'.join([userMajor, userMinor.userBuild]),
                "link": versions_list[userMajor][userMinor][userBuild]
            }
        if founded:
            raise Exception(founded)
        if strict and userBuild != "999":
            return None
        if userMajor in versions_list and userMinor in versions_list[userMajor]:
            build = max(versions_list[userMajor][userMinor].keys()).__str__()
            founded = {
                "version": '.'.join([userMajor, userMinor, build]),
                "link": versions_list[userMajor][userMinor][build]
            }
        if founded:
            raise Exception(founded)
        if strict and userMinor != "999":
            return None
        if userMajor in versions_list:
            minor = max(versions_list[userMajor].keys()).__str__()
            build = max(versions_list[userMajor][minor].keys()).__str__()
            founded = {
                "version": '.'.join([userMajor, minor, build]),
                "link": versions_list[userMajor][minor][build]
            }
        if founded:
            raise Exception(founded)
        if not founded:
            return

    try:
        is_64bits = sys.maxsize > 2 ** 32
        if is_64bits:
            find(versions['releases']['64'])
            find(versions['archived']['64'])
        find(versions['releases']['86'])
        find(versions['archived']['86'])

        if is_64bits:
            find(versions['releases']['64'], False)
            find(versions['archived']['64'], False)
        find(versions['releases']['86'], False)
        find(versions['archived']['86'], False)
        raise Exception(None)
    except Exception as e:
        return e.args[0]
    pass


@simple_cache(CACHE, 3600, "php")
def getPhpVersions():
    versions = {}
    regex = r"^ts-(.{4})-x(86|64)$"
    versions['releases'] = {
        "64": {},
        "86": {}
    }
    versions['archived'] = {
        "64": {},
        "86": {}
    }
    if VERBOSE:
        print(f"Load data from {phpBaseAddress}")
    try:
        data = json.loads(requests.get(phpBaseAddress + "releases.json").content)
        for v in data:
            versionData = data[v]
            v = Version(versionData['version'])
            for key in versionData:
                matches = re.search(regex, key)
                if matches:
                    groups = matches.groups()
                    if len(groups):
                        arch = groups[1]
                        name = versionData[key]["zip"]['path']
                        major = v.get_major_version().__str__()
                        minor = v.get_minor_version().__str__()
                        build = v.get_build_version().__str__()
                        if major not in versions['releases'][arch]:
                            versions['releases'][arch][major] = {}
                        if minor not in versions['releases'][arch][major]:
                            versions['releases'][arch][major][minor] = {}
                        if build not in versions['releases'][arch][major][minor]:
                            versions['releases'][arch][major][minor][build] = {}
                        versions['releases'][arch][major][minor][build] = f"https://windows.php.net/downloads/releases/{name}"
                        pass
    except ValueError:
        pass
    try:
        regex = r"^php-(\d+\.\d+\.\d+)-Win32-(.+?)-x(86|64)\.zip$"
        root = BeautifulSoup(requests.get(phpBaseAddress + "archives/").content, 'html.parser')
        links = root.select('pre a')
        for link in links:
            matches = re.search(regex, link.text)
            if matches:
                groups = matches.groups()
                v = Version(groups[0])
                arch = groups[2]
                major = v.get_major_version().__str__()
                minor = v.get_minor_version().__str__()
                build = v.get_build_version().__str__()
                if major not in versions['archived'][arch]:
                    versions['archived'][arch][major] = {}
                if minor not in versions['archived'][arch][major]:
                    versions['archived'][arch][major][minor] = {}
                if build not in versions['archived'][arch][major][minor]:
                    versions['archived'][arch][major][minor][build] = {}
                versions['archived'][arch][major][minor][build] = f"https://windows.php.net/downloads/releases/archives/{link.text}"
    except ValueError:
        pass
    # pprint.pprint(versions)
    return versions
    pass
