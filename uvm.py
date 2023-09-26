import os

import cement.ext.ext_argparse
import cement.ext.ext_configparser
import cement.ext.ext_dummy
import cement.ext.ext_logging
import cement.ext.ext_plugin
import cement.ext.ext_smtp
from cement import App

from src.cli.nodeCli import NodeCli
from src.cli.phpСli import PhpCli
from src.config import PROGRAM_PATH, NODE_PATH, PHP_PATH, BIN_PATH, CACHE_PATH, TO_PATH_PATH
from src.utils import download


# MAST HAVE
# import cement.ext.ext_dummy
# import cement.ext.ext_smtp
# import cement.ext.ext_plugin
# import cement.ext.ext_configparser
# import cement.ext.ext_logging
# import cement.ext.ext_argparse


def install():
    os.makedirs(PROGRAM_PATH, exist_ok=True)
    os.makedirs(NODE_PATH, exist_ok=True)
    os.makedirs(PHP_PATH, exist_ok=True)
    os.makedirs(BIN_PATH, exist_ok=True)
    os.makedirs(CACHE_PATH, exist_ok=True)
    download(filename=TO_PATH_PATH,
             url="https://github.com/Traineratwot/toPath/releases/download/1.2.0/toPath.exe")


class UVM(App):
    class Meta:
        label = 'UVM'
        handlers = [
            NodeCli,
            PhpCli,
        ]


if __name__ == '__main__':
    a1 = cement.ext.ext_dummy
    a2 = cement.ext.ext_smtp
    a3 = cement.ext.ext_plugin
    a4 = cement.ext.ext_configparser
    a5 = cement.ext.ext_logging
    a6 = cement.ext.ext_argparse
    if not os.path.exists(PROGRAM_PATH):
        install()
    with UVM() as app:
        app.run()
