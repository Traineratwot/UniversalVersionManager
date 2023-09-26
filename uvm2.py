import argparse
import os

from termcolor import colored

from src.argparse.Namespace import argparse.Namespace
from src.config import PROGRAM_PATH, BIN_PATH, TO_PATH_PATH, NODE_PATH, PHP_PATH, CACHE_PATH
from src.lang import _
from src.utils import download

TEST = False


def install():
    os.makedirs(PROGRAM_PATH, exist_ok=True)
    os.makedirs(NODE_PATH, exist_ok=True)
    os.makedirs(PHP_PATH, exist_ok=True)
    os.makedirs(BIN_PATH, exist_ok=True)
    os.makedirs(CACHE_PATH, exist_ok=True)
    download(filename=TO_PATH_PATH,
             url="https://github.com/Traineratwot/toPath/releases/download/1.2.0/toPath.exe")


def route(args_):
    args2 = argparse.Namespace(args_)
    match args2.service:
        case 'node':
            from src.service.Node import Node
            print(Node().callByName(args2.action, argparse.Namespace(args2)))
        case 'php':
            from src.service.Php import Php
            print(Php().callByName(args2.action, argparse.Namespace(args2)))
            pass
        case 'python':
            pass
        case _:
            print(_("unknown") + " " + args2.service)
    pass


if __name__ == '__main__':
    if not os.path.exists(PROGRAM_PATH):
        install()

    parser = argparse.ArgumentParser(
        prog='UVM',
        description='Universal Version Manager',
        epilog='Thanks for use :)'
    )

    parser.add_argument("service", choices=['node', 'php', 'python'], help=colored(_("help.service"))
    actions = {
        'use': colored(_("help.select"), "light_blue"),
        'off': colored(_("help.off"), "light_blue"),
        'list': colored(_("help.list"), "light_blue"),
        'install': colored(_("help.install"), "light_blue"),
        'remove': colored(_("help.remove"), "light_blue"),
        'path': colored(_("help.path"), "light_blue"),
        'search': colored(_("help.search"), "light_blue"),
        'addGlobal': colored(_("help.addGlobal"), "light_blue"),
    }
    _help = []
    for h in actions:
        _help.append(f"{h} {actions[h]}")
    helpStr = ";\n".join(_help)

    parser.add_argument("action", choices=actions.keys(), help=helpStr, metavar='Action')
    parser.add_argument("version", default=None, nargs='?', metavar='Version', help=F"{colored(_('help.version'), 'light_blue')}")

    args = parser.parse_args()

    route(args)
