import argparse
import os.path
import shutil
import sys

import questionary
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from version_parser import Version

from abstractService import abstractService
from config import NODE_PATH, BIN_PATH, SEP, VERBOSE
from utils import find_max_version, download, addToPath, removeToPath, cmd, createSymlink, \
    removeSymlink, strToVersion

nodeBaseAddress = "https://nodejs.org/dist/"
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
        version = find_max_version(args.version, getVersions().keys())
        href = getVersions()[version]
        name = f"node-v{version}-win-x{64 if is_64bits else 86}"
        href = href + name + ".zip"
        # Скачивает node
        download(filename=NODE_PATH + version, url=href, kind='zip')

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
        version = find_max_version(args.version, getVersions().keys())
        folder = NODE_PATH + version + os.path.sep
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
        my_table.add_column("url", '')
        search_list = {}

        def custom_sort(item):
            return Version(strToVersion(item))

        _versionKeys = sorted(_versions.keys(), key=custom_sort, reverse=True)
        for version in _versionKeys:
            try:
                v = Version(strToVersion(version))
                m = v.get_major_version()
                if m not in search_list:
                    search_list[m] = []
                search_list[m] += [v.__str__()]
            except ValueError:
                pass
        if args.version:
            m = Version(strToVersion(args.version)).get_major_version()
            if m in search_list:
                for version in search_list[m]:
                    if args.version in version:
                        my_table.add_row([version, _versions[version]])
        else:
            for majors in search_list:
                maxVersion = search_list[majors][0]
                my_table.add_row([maxVersion, _versions[maxVersion]])
        return my_table
        pass


def getVersions():
    if len(versions.keys()) > 0:
        return versions
    html = requests.get(nodeBaseAddress).content
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('pre a')
    for link in links:
        if link.attrs['href']:
            try:
                href = nodeBaseAddress + link.attrs['href']
                version = link.text.strip('latest-v/.x')
                Version(strToVersion(version))
                versions[version] = href
            except ValueError:
                pass

    return versions
    pass


def printCurrentVersions():
    node = cmd("node -v")
    npm = cmd("npm -v")
    return f"""{'Now used node ' + node[0] if len(node) >= 1 else "node use error"}
{'Now used npm ' + npm[0] if len(npm) >= 1 else "node use error"}"""
