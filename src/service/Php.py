import json
import os
import re
import shutil
import sys
from os.path import join, dirname, exists

import questionary
import requests
from SimpleCache2 import simple_cache
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from version_parser import Version

from src.AbstractService import AbstractService
from src.cache import MEMORY, SETTINGS, CACHE
from src.config import VERBOSE, PHP_PATH, BIN_PATH
from src.lang import _
from src.stat import sendStat
from src.utils import strToVersion, download, removeSymlink, createSymlink, saveUse, cmd, removeToPath, addToPath, \
    getUsed, is_process_running, file_get_contents, file_put_contents, Args

phpBaseAddress = "https://windows.php.net/downloads/releases/"


class Php(AbstractService):
    """Управление php"""

    def setup(self):
        if not os.path.exists(PHP_PATH):
            os.mkdir(PHP_PATH)
        phpBin = join(BIN_PATH, 'php', 'php.exe')
        # Настройка Path
        if self.OpenServer():
            pass
        else:
            allPhp = cmd("where php")
            if len(allPhp) > 1 or (len(allPhp) == 1 and allPhp[0] != phpBin):
                my_table = PrettyTable()
                for item in allPhp:
                    my_table.add_row([item])
                answer = True
                if not VERBOSE:
                    q = questionary.confirm(_('ask.alternative', 'php', my_table))
                    answer = q.ask()
                if answer:
                    # Интеграция с nvm
                    if len(cmd("where pvm")):
                        os.system("pvm clear")
                        allPhp = cmd("where php")
                    for item in allPhp:
                        if item != join(BIN_PATH, 'php'):
                            removeToPath(os.path.dirname(item))
                        pass
                    addToPath(join(BIN_PATH, 'php'))

                else:
                    pass
                pass
            else:
                addToPath(join(BIN_PATH, 'php'))
                if SETTINGS.get('OpenServerIntegrated'):
                    if not os.environ.get('PHP_DIR'):
                        command = f'SETX PHP_DIR %s' % dirname(BIN_PATH)
                        if VERBOSE:
                            print(command)
                        os.system(command)
                    if not os.environ.get('PHP_BIN'):
                        command = f'SETX PHP_BIN %s' % BIN_PATH
                        if VERBOSE:
                            print(command)
                        os.system(command)
                pass

    def OpenServer(self) -> bool:
        osPath = self.OpenServerExits()
        if osPath:
            if not SETTINGS.exist('OpenServerIntegrated'):
                answer = True
                if not VERBOSE:
                    q = questionary.confirm(_('ask.OpenServer'))
                    answer = q.ask()
                SETTINGS.set('OpenServerIntegrated', answer)
                SETTINGS.set('OpenServerPath', osPath)
                sendStat('open_server', {"on": answer})
                return answer
            pass
        else:
            SETTINGS.set('OpenServerIntegrated', False)
        return False
        pass

    # noinspection PyMethodMayBeStatic
    def OpenServerExits(self):
        path = is_process_running("Open Server Panel.exe") or is_process_running("Open Server.exe")
        if path:
            return dirname(path)
        allPhp = cmd("where php")
        if len(allPhp) > 1 or (len(allPhp) == 1 and ("OSPanel" in allPhp[0] or "openserver" in allPhp[0])):
            path = dirname(dirname(dirname(allPhp[0])))
            return path
            pass
        return False
        pass

    def use(self, args):
        if 'version' in args and args.version:
            v = getPhpVersionFromUserRequest(args)
            if v:
                path = self.path(args)
                if path:
                    if not os.path.exists(path):
                        self.install(args)
                    if not os.path.exists(path):
                        return 'error'
                    removeSymlink(join(BIN_PATH, 'php'))
                    createSymlink(
                        target_dir=join(BIN_PATH, 'php'),
                        source_dir=path
                    )
                    saveUse('php', v['version'])
                    return printCurrentPhpVersions()
            return _("err.versionNotFound", args.version)
        else:
            return printCurrentPhpVersions()
        pass
        pass

    def off(self, args):
        removeSymlink(join(BIN_PATH, 'php'))
        pass

    def list(self, args):
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

    def install(self, args):
        v = getPhpVersionFromUserRequest(args)
        if v:
            print(v['link'])
            if v['link'].startswith('http'):
                download(filename=join(PHP_PATH, v['version']), url=v['link'], kind='zip')
            else:
                if os.path.exists(join(PHP_PATH, v['version'])) and not os.path.islink(join(PHP_PATH, v['version'])):
                    shutil.rmtree(join(PHP_PATH, v['version']))
                createSymlink(
                    target_dir=join(PHP_PATH, v['version']),
                    source_dir=v['link']
                )

            sendStat('php_install', {'version': v['version']})

        return 'install'
        pass

    def remove(self, args):
        path = self.path(args)
        if path:
            answer = True
            if not VERBOSE:
                q = questionary.confirm(f"Delete this '{path}' ?")
                answer = q.ask()
            if answer:
                shutil.rmtree(path)
                sendStat('php_remove', {'version': os.path.basename(path)})
                return f'removed {path}'
            return 'canceled'
        return 'already removed'
        pass

    def path(self, args):
        if not args.version:
            current = getUsed('node')
            args = Args()
            args.version = current
        v = getPhpVersionFromUserRequest(args)
        if v:
            return join(PHP_PATH, v['version'])
        pass

    def search(self, args):
        my_table = PrettyTable()
        my_table.add_column(_("arch"), '')
        my_table.add_column(_("version"), '')
        my_table.add_column(_("released"), '')

        versions = getPhpVersions()
        is_64bits = sys.maxsize > 2 ** 32
        m = None
        if 'version' in args and args.version:
            m = Version(strToVersion(args.version))

        def parse(_versions, r):
            for arch in _versions:
                if not is_64bits and arch == "64":
                    continue
                for major in _versions[arch]:
                    if m and m.get_major_version() != 999 and m.get_major_version().__str__() != major:
                        continue
                    for minor in _versions[arch][major]:
                        if m and m.get_minor_version() != 999 and m.get_minor_version().__str__() != minor:
                            continue
                        for build in _versions[arch][major][minor]:
                            v = Version(f"{major}.{minor}.{build}")
                            if m and m.get_build_version() != 999 and m.get_build_version().__str__() != build:
                                continue
                            my_table.add_row([arch, v, r])
                            pass

        parse(versions['OpenServer'], "OpenServer")
        parse(versions['releases'], True)
        parse(versions['archived'], False)

        return my_table
        pass

    # noinspection PyMethodMayBeStatic
    def addGlobal(self, args):
        packageList = set(args.packages)
        if not len(packageList):
            my_table = PrettyTable()
            my_table.add_column(_("package"), '')
            if exists(join(PHP_PATH, "global.package")):
                packages = file_get_contents(join(PHP_PATH, "global.package")).strip()
                packages = set(packages.split("\n"))

                for package in packages:
                    my_table.add_row([package])
            return my_table
        packages = set()
        if exists(join(PHP_PATH, "global.package")):
            packages = file_get_contents(join(PHP_PATH, "global.package")).strip()
            packages = set(packages.split("\n"))
        for package in packageList:
            print(f"composer global require -g {package}")
            code = os.system(f"composer global require {package}")
            if code == 0:
                packages.add(package)
            file_put_contents(join(PHP_PATH, "global.package"), "\n".join(packages))
            file_put_contents(join(BIN_PATH, "php", "global.package"), "\n".join(packages))
        sendStat('php_global', {'packages': packageList})
        return "ok"
        pass


def printCurrentPhpVersions():
    php = cmd("php -v")
    return _('used', 'php', php[0] if len(php) >= 1 else "php use error")
    pass


@simple_cache(MEMORY, 0, "php")
def getPhpVersionFromUserRequest(args):
    versions = getPhpVersions()
    version = Version(strToVersion(args.version))
    userMajor = version.get_major_version().__str__()
    userMinor = version.get_minor_version().__str__()
    userBuild = version.get_build_version().__str__()

    def find(versions_list, strict=True, release=None):
        founded = None
        if userMajor.__str__() not in versions_list:
            return None
        if userMajor in versions_list and userMinor in versions_list[userMajor] and userBuild in \
                versions_list[userMajor][userMinor]:
            founded = {
                "version": '.'.join([userMajor, userMinor, userBuild]),
                "link": versions_list[userMajor][userMinor][userBuild],
                "release": release
            }
        if founded:
            raise Exception(founded)
        if strict and userBuild != "999":
            return None
        if userMajor in versions_list and userMinor in versions_list[userMajor]:
            build = max(versions_list[userMajor][userMinor].keys()).__str__()
            founded = {
                "version": '.'.join([userMajor, userMinor, build]),
                "link": versions_list[userMajor][userMinor][build],
                "release": release
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
                "link": versions_list[userMajor][minor][build],
                "release": release
            }
        if founded:
            raise Exception(founded)
        if not founded:
            return

    try:
        is_64bits = sys.maxsize > 2 ** 32
        if is_64bits:
            find(versions['OpenServer']['64'], release='OpenServer')
            find(versions['releases']['64'], release='releases')
            find(versions['archived']['64'], release='archived')
        find(versions['releases']['86'], release='releases')
        find(versions['archived']['86'], release='archived')

        if is_64bits:
            find(versions['OpenServer']['64'], False, release='OpenServer')
            find(versions['releases']['64'], False, release='releases')
            find(versions['archived']['64'], False, release='archived')
        find(versions['releases']['86'], False, release='releases')
        find(versions['archived']['86'], False, release='archived')
        raise Exception(None)
    except Exception as e:
        return e.args[0]
    pass


@simple_cache(CACHE, 3600, "php")
def getPhpVersions():
    versions = {}
    regex = r"^ts-(.{4})-x(86|64)$"
    versions['OpenServer'] = {
        "64": {},
    }
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
        data = json.loads(requests.get(phpBaseAddress + "releases.json", verify=False).content)
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
                        versions['releases'][arch][major][minor][
                            build] = f"https://windows.php.net/downloads/releases/{name}"
                        pass
    except ValueError:
        pass
    try:
        regex = r"^php-(\d+\.\d+\.\d+)-Win32-(.+?)-x(86|64)\.zip$"
        root = BeautifulSoup(requests.get(phpBaseAddress + "archives/", verify=False).content, 'html.parser')
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
                versions['archived'][arch][major][minor][
                    build] = f"https://windows.php.net/downloads/releases/archives/{link.text}"
    except ValueError:
        pass
    try:
        if SETTINGS.get('OpenServerIntegrated'):
            files = os.scandir(join(SETTINGS.get('OpenServerPath'), 'modules', 'php'))
            for file in files:
                regex = r"PHP_(\d+)\.(\d+)"
                matches = re.search(regex, file.name)
                arch = '64'
                major = matches[1]
                minor = matches[2]
                build = '0'
                if major not in versions['OpenServer'][arch]:
                    versions['OpenServer'][arch][major] = {}
                if minor not in versions['OpenServer'][arch][major]:
                    versions['OpenServer'][arch][major][minor] = {}
                if build not in versions['OpenServer'][arch][major][minor]:
                    versions['OpenServer'][arch][major][minor][build] = {}
                versions['OpenServer'][arch][major][minor][build] = file.path
            pass
    except ValueError:
        pass
    return versions
    pass
