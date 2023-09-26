import filecmp
import json
import os.path
import shutil
import sys
from functools import lru_cache
from os.path import exists, join

import questionary
import requests
from SimpleCache2 import simple_cache
from prettytable import PrettyTable
from version_parser import Version

from src.AbstractService import AbstractService
from src.config import NODE_PATH, BIN_PATH, VERBOSE, CACHE
from src.lang import _
from src.utils import download, addToPath, removeToPath, cmd, createSymlink, \
    removeSymlink, strToVersion, file_get_contents, file_put_contents, saveUse, getUsed

nodeBaseAddress = "https://nodejs.org/dist/"
nodeReleasesAddress = "https://nodejs.org/dist/index.json"


class Node(AbstractService):
    """Управление node и npm """

    def off(self, args):
        removeSymlink(join(BIN_PATH, 'node'))

    def setup(self):
        nodeBin = join(BIN_PATH, 'node', 'node.exe')
        # Настройка Path
        allNodes = cmd("where node")
        if len(allNodes) > 1 or (len(allNodes) == 1 and allNodes[0] != nodeBin):
            my_table = PrettyTable()
            for item in allNodes:
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
                if len(cmd("where nvm")):
                    os.system("nvm off")
                    allNodes = cmd("where node")
                for item in allNodes:
                    if item != join(BIN_PATH, 'node'):
                        removeToPath(os.path.dirname(item))
                    pass
                addToPath(join(BIN_PATH, 'node'))
            else:
                exit(1)
                pass
            pass
        else:
            addToPath(join(BIN_PATH, 'node'))
            pass
        # Настройка bin

        pass

    def use(self, args):
        if args.version:
            v = getNodeVersionFromUserRequest(args)
            path = self.path(args)
            if not path:
                self.install(args)

            path = self.path(args)
            if not path:
                return 'error'
            removeSymlink(join(BIN_PATH, 'node'))
            createSymlink(
                target_dir=join(BIN_PATH, 'node'),
                source_dir=path
            )
            saveUse('node', v['version'])
            if exists(join(NODE_PATH, "global.package")):
                if not exists(join(path, "global.package")) or not filecmp.cmp(join(NODE_PATH, "global.package"), join(path, "global.package")):
                    packages = set(file_get_contents(join(NODE_PATH, "global.package")).strip().split("\n"))
                    packages_old = set()
                    if exists(join(path, "global.package")):
                        packages_old = set(file_get_contents(join(path, "global.package")).strip().split("\n"))
                    diff = packages - packages_old
                    for package in diff:
                        os.system(f"npm install -g {package}")
                    shutil.copyfile(join(NODE_PATH, "global.package"), join(path, "global.package"))
            return printCurrentNodeVersions()
        else:
            return printCurrentNodeVersions()
        pass

    def list(self, args):
        dirs = os.scandir(NODE_PATH)
        my_table = PrettyTable()
        my_table.add_column("Version", "")
        current = getUsed('node')
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
        is_64bits = sys.maxsize > 2 ** 32
        v = getNodeVersionFromUserRequest(args)
        name = f"node-{v['version']}-win-x{64 if is_64bits else 86}"
        href = nodeBaseAddress + v['version'] + "/" + name + ".zip"
        # Скачивает node
        download(filename=join(NODE_PATH, v['version']), url=href, kind='zip')

        return 'install'
        pass

    def remove(self, args):
        path = self.path(args)
        if path:
            path = os.path.dirname(os.path.dirname(path))
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

    def path(self, args):
        if not args.version:
            return "need version"
        v = getNodeVersionFromUserRequest(args)
        folder = join(NODE_PATH, v['version'])
        if exists(folder):
            with os.scandir(folder) as it:
                for entry in it:
                    if not entry.name.startswith('.'):
                        folder = join(folder, entry.name)
                        break
            return folder
        return None
        pass

    def search(self, args):
        versions = getNodeVersions()
        my_table = PrettyTable()
        my_table.add_column(_("version"), '')
        my_table.add_column(_("lts"), '')
        if args.version:
            m = Version(strToVersion(args.version)).get_major_version().__str__()
            if m in versions['list']:
                for version in versions['list'][m]:
                    if args.version in version['version']:
                        my_table.add_row([version['version'], version['lts']])
        else:
            for lts in versions['lts']:
                my_table.add_row([versions['lts'][lts]['version'], True])
        return my_table
        pass

    def addGlobal(self, args):
        packageList = set(args.version.split(" "))
        packages = set()
        if exists(join(NODE_PATH, "global.package")):
            packages = file_get_contents(join(NODE_PATH, "global.package")).strip()
            packages = set(packages.split("\n"))
        for package in packageList:
            print(f"npm install -g {package}")
            code = os.system(f"npm install -g {package}")
            if code == 0:
                packages.add(package)
            file_put_contents(join(NODE_PATH, "global.package"), "\n".join(packages))
            file_put_contents(join(BIN_PATH, "node", "global.package"), "\n".join(packages))
        return "ok"
        pass

    def customCallByName(self, func_name: str, args):
        match func_name:
            case 'addGlobal':
                return self.addGlobal(args)
        pass


def getNodeVersionFromUserRequest(args):
    versions = getNodeVersions()
    version = Version(strToVersion(args.version))
    userMajor = version.get_major_version()
    userMinor = version.get_minor_version()
    userBuild = version.get_build_version()
    founded = None
    if userMajor.__str__() not in versions['list']:
        raise Exception(f"unknown Major version: {userMajor.__str__()}")
    for version in versions['list'][userMajor.__str__()]:
        v = Version(version['version'])
        listMajor = v.get_major_version()
        listMinor = v.get_minor_version()
        listBuild = v.get_build_version()
        if listMajor == userMajor and listMinor == userMinor and listBuild == userBuild:
            founded = version
    if founded:
        return founded
    else:
        for version in versions['list'][userMajor.__str__()]:
            v = Version(version['version'])
            listMajor = v.get_major_version()
            listMinor = v.get_minor_version()
            if listMajor == userMajor and listMinor == userMinor:
                founded = version
    if founded:
        return founded
    else:
        for version in versions['list'][userMajor.__str__()]:
            v = Version(version['version'])
            listMajor = v.get_major_version()
            if listMajor == userMajor and version['lts']:
                founded = version
    if founded:
        return founded
    else:
        for version in versions['list'][userMajor.__str__()]:
            v = Version(version['version'])
            listMajor = v.get_major_version()
            if listMajor == userMajor:
                return version
    pass


@simple_cache(CACHE, 3600, "node")
def getNodeVersions():
    versions = {}
    try:
        versions['lts'] = {}
        versions['list'] = {}
        if VERBOSE:
            print(f"Load data from {nodeReleasesAddress}")
        data = json.loads(requests.get(nodeReleasesAddress).content)
        for versionData in data:
            v = Version(versionData['version'])
            major = v.get_major_version().__str__()
            if major not in versions['list']:
                versions['list'][major] = []
            versions['list'][major].append(versionData)
            if versionData['lts']:
                if major not in versions['lts']:
                    versions['lts'][major] = versionData
    except ValueError:
        pass
    # pprint.pprint(versions)
    return versions
    pass


def printCurrentNodeVersions():
    node = cmd("node -v")
    npm = cmd("npm -v")
    return _('used', 'node', node[0] if len(node) >= 1 else "node use error") + "\n" + _('used', 'npm', npm[0] if len(npm) >= 1 else "npm use error")
