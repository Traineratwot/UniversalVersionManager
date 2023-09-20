import argparse
import os.path
import sys

import questionary
import requests
from prettytable import PrettyTable
from termcolor import colored

from abstractService import abstractService
from bs4 import BeautifulSoup

from config import PROGRAM_PATH, NODE_PATH, BIN_PATH
from utils import find_max_version, download, addToPath, removeToPath, cmd

nodeBaseAddress = "https://nodejs.org/dist/"
versions = {}


class Node(abstractService):
    """A simple example class"""

    def setup(self):
        nodeBin = BIN_PATH + 'node.bat'
        # Настройка Path
        allNodes = cmd("where node")
        if len(allNodes) > 1 or (len(allNodes) == 1 and allNodes[0] != nodeBin):
            my_table = PrettyTable()
            for item in allNodes:
                my_table.add_row([item])
            answer = questionary.confirm(f"""
Alternative installations have been found:
{my_table}
Do you want to replace them?
""").ask()
            if answer:
                # Интеграция с nvm
                if len(cmd("where nvm")):
                    os.system("nvm off")
                    allNodes = cmd("where node")
                for item in allNodes:
                    if item != BIN_PATH:
                        removeToPath(os.path.dirname(item))
                    pass
                addToPath(BIN_PATH)
            else:
                exit(1)
                pass
            pass
        else:
            addToPath(BIN_PATH)
            pass
        # Настройка bin

        pass

    def use(self, args: argparse.Namespace):

        return 'use'
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
        return 'remove'
        pass

    def path(self, args: argparse.Namespace):
        if not args.version:
            raise "need version"
        version = find_max_version(args.version, getVersions().keys())
        folder = NODE_PATH + version + os.path.sep
        with os.scandir(folder) as it:
            for entry in it:
                if not entry.name.startswith('.'):
                    folder = folder + entry.name
                    break
        return folder + os.path.sep
        pass

    def search(self, args: argparse.Namespace):

        versions = getVersions()
        my_table = PrettyTable()

        versions.keys()

        for version in versions.keys():
            my_table.add_row([version, versions[version]])
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
            if link.text.startswith("v") or link.text.startswith("latest"):
                if link.text.startswith("v0"):
                    continue
                href = nodeBaseAddress + link.attrs['href']
                version = link.text.strip('latest-v/.x')
                versions[version] = href
    return versions
    pass
