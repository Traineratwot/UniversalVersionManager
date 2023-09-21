import argparse
import os

from termcolor import colored

from config import PROGRAM_PATH, BIN_PATH, TO_PATH_PATH
from service import Node
from utils import download


def install():
    os.mkdir(PROGRAM_PATH)
    os.mkdir(BIN_PATH)
    download(filename=TO_PATH_PATH,
             url="https://github.com/Traineratwot/toPath/releases/download/1.2.0/toPath.exe")


def route(args: argparse.Namespace):
    match args.service:
        case 'node':
            service = Node.Node().callByName(args.action, args)
            print(service)
        case 'php':
            pass
        case 'python':
            pass
        case _:
            print("Unknown " + args.service)
    pass


if __name__ == '__main__':
    if not os.path.exists(PROGRAM_PATH):
        install()

    parser = argparse.ArgumentParser(
        prog='UVM',
        description='Universal Version Manager',
        epilog='Thanks for use :)'
    )

    parser.add_argument("service", choices=['node', 'php', 'python'])
    parser.add_argument("action", choices=['use', 'list', 'install', 'remove', 'search', 'path', 'off'], help=f"""
    {colored("use", "green")}       -   {colored("select version to use", "light_blue")};\n
    {colored("off", "green")}       -   {colored("deselect any version", "light_blue")};\n
    {colored("list", "green")}      -   {colored("show all available versions", "light_blue")};\n
    {colored("install", "green")}   -   {colored("install new version", "light_blue")};\n
    {colored("remove", "green")}    -   {colored("remove version", "light_blue")};\n
    {colored("path", "green")}      -   {colored("get path to source folder", "light_blue")};\n
    {colored("search", "green")}    -   {colored("shows all versions available for installation", "light_blue")};\n
    """, metavar='Action')
    parser.add_argument("version", default=None, nargs='?', metavar='Version',
                        help=F"{colored('version string', 'light_blue')}")

    args = parser.parse_args()

    route(args)
