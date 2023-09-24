import argparse
import os

from termcolor import colored

from Arguments import Arguments
from config import PROGRAM_PATH, BIN_PATH, TO_PATH_PATH
from utils import download

TEST = False


def install():
    os.mkdir(PROGRAM_PATH)
    os.mkdir(BIN_PATH)
    download(filename=TO_PATH_PATH,
             url="https://github.com/Traineratwot/toPath/releases/download/1.2.0/toPath.exe")


def route(args_: argparse.Namespace):
    args2 = Arguments(args_)
    match args2.service:
        case 'node':
            from service.Node import Node
            print(Node().callByName(args2.action, Arguments(args2)))
        case 'php':
            from service.Php import Php
            print(Php().callByName(args2.action, Arguments(args2)))
            pass
        case 'python':
            pass
        case _:
            print("Unknown " + args2.service)
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
    actions = {
        'use': colored("select version to use", "light_blue"),
        'off': colored("select version to use", "light_blue"),
        'list': colored("show all available versions", "light_blue"),
        'install': colored("install new version", "light_blue"),
        'remove': colored("remove version", "light_blue"),
        'path': colored("get path to source folder", "light_blue"),
        'search': colored("shows all versions available for installation", "light_blue"),
        'addGlobal': colored("(node) add a global package to all versions, for example: typescript", "light_blue"),
    }
    _help = []
    for h in actions:
        _help.append(f"{h} {actions[h]}")
    helpStr = ";\n".join(_help)

    parser.add_argument("action", choices=actions.keys(), help=helpStr, metavar='Action')
    parser.add_argument("version", default=None, nargs='?', metavar='Version', help=F"{colored('version string', 'light_blue')}")

    args = parser.parse_args()

    route(args)
