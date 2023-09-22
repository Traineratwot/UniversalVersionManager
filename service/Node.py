import argparse
import json
import os.path
import pprint
import shutil
import sys

import questionary
import requests
from prettytable import PrettyTable
from version_parser import Version

from abstractService import abstractService
from config import NODE_PATH, BIN_PATH, SEP, VERBOSE
from utils import download, addToPath, removeToPath, cmd, createSymlink, \
    removeSymlink, strToVersion

nodeBaseAddress = "https://nodejs.org/dist/"
nodeReleasesAddress = "https://nodejs.org/dist/index.json"
versions = {}


class Node(abstractService):
    """Управлене node и npm """

    def off(self, args: argparse.Namespace):
        removeSymlink(BIN_PATH + 'node')

    def setup(self):
        nodeBin = BIN_PATH + 'node' + SEP + 'node.exe'
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
                    if item != BIN_PATH + 'node':
                        removeToPath(os.path.dirname(item))
                    pass
                addToPath(BIN_PATH + 'node')
            else:
                exit(1)
                pass
            pass
        else:
            addToPath(BIN_PATH + 'node')
            pass
        # Настройка bin

        pass

    def use(self, args: argparse.Namespace):
        if args.version:
            path = self.path(args)
            if not path:
                self.install(args)

            path = self.path(args)
            if not path:
                return 'error'
            removeSymlink(BIN_PATH + 'node')
            createSymlink(
                target_dir=BIN_PATH + 'node',
                source_dir=path
            )
            return printCurrentVersions()
        else:
            return printCurrentVersions()
        pass

    def list(self, args: argparse.Namespace):
        return 'list'
        pass

    def install(self, args: argparse.Namespace):
        is_64bits = sys.maxsize > 2 ** 32
        v = getVersionFromUserRequest(args)
        name = f"node-{v['version']}-win-x{64 if is_64bits else 86}"
        href = nodeBaseAddress + v['version'] + "/" + name + ".zip"
        # Скачивает node
        download(filename=NODE_PATH + v['version'], url=href, kind='zip')

        return 'install'
        pass

    def remove(self, args: argparse.Namespace):
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

    def path(self, args: argparse.Namespace):
        if not args.version:
            raise "need version"
        v = getVersionFromUserRequest(args)
        folder = NODE_PATH + v['version'] + os.path.sep
        if os.path.exists(folder):
            with os.scandir(folder) as it:
                for entry in it:
                    if not entry.name.startswith('.'):
                        folder = folder + entry.name
                        break
            return folder + os.path.sep
        return None
        pass

    def search(self, args: argparse.Namespace):
        _versions = getVersions()
        my_table = PrettyTable()
        my_table.add_column("version", '')
        my_table.add_column("lts", '')
        if args.version:
            m = Version(strToVersion(args.version)).get_major_version().__str__()
            if m in _versions['list']:
                for version in _versions['list'][m]:
                    if args.version in version['version']:
                        my_table.add_row([version['version'], version['lts']])
        else:
            for lts in _versions['lts']:
                my_table.add_row([_versions['lts'][lts]['version'], True])
        return my_table
        pass


def getVersionFromUserRequest(args: argparse.Namespace):
    _versions = getVersions()
    version = Version(strToVersion(args.version))
    userMajor = version.get_major_version()
    userMinor = version.get_minor_version()
    userBuild = version.get_build_version()
    founded = None
    for version in _versions['list'][userMajor.__str__()]:
        v = Version(version['version'])
        listMajor = v.get_major_version()
        listMinor = v.get_minor_version()
        listBuild = v.get_build_version()
        if listMajor == userMajor and listMinor == userMinor and listBuild == userBuild:
            founded = version
    if founded:
        return founded
    else:
        for version in _versions['list'][userMajor.__str__()]:
            v = Version(version['version'])
            listMajor = v.get_major_version()
            listMinor = v.get_minor_version()
            if listMajor == userMajor and listMinor == userMinor:
                founded = version
    if founded:
        return founded
    else:
        for version in _versions['list'][userMajor.__str__()]:
            v = Version(version['version'])
            listMajor = v.get_major_version()
            if listMajor == userMajor and version['lts']:
                founded = version
    if founded:
        return founded
    else:
        for version in _versions['list'][userMajor.__str__()]:
            v = Version(version['version'])
            listMajor = v.get_major_version()
            if listMajor == userMajor:
                return version
    pass


def getVersions():
    if len(versions.keys()) > 0:
        return versions
    try:
        versions['lts'] = {}
        versions['list'] = {}
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


def printCurrentVersions():
    node = cmd("node -v")
    npm = cmd("npm -v")
    return f"""{'Now used node ' + node[0] if len(node) >= 1 else "node use error"}
{'Now used npm ' + npm[0] if len(npm) >= 1 else "node use error"}"""
