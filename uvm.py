import os
import shutil
import subprocess
import sys
from os.path import join

import cement.ext.ext_argparse
import cement.ext.ext_configparser
import cement.ext.ext_dummy
import cement.ext.ext_logging
import cement.ext.ext_plugin
import cement.ext.ext_smtp
import questionary
from cement import App, ex, Controller

from src.cli.nodeCli import NodeCli
from src.cli.phpСli import PhpCli
from src.config import PROGRAM_PATH, NODE_PATH, PHP_PATH, BIN_PATH, CACHE_PATH, TO_PATH_PATH, VERBOSE
from src.lang import _
from src.utils import download, addToPath, removeToPath


# MAST HAVE
# import cement.ext.ext_dummy
# import cement.ext.ext_smtp
# import cement.ext.ext_plugin
# import cement.ext.ext_configparser
# import cement.ext.ext_logging
# import cement.ext.ext_argparse

class Base(Controller):
    """Cli node"""

    class Meta:
        label = 'base'

    @ex(hide=True)
    def _default(self):
        if self.install():
            super()._default()

    @ex(
        help=_("help.base.install"),
    )
    def install(self):
        print(sys.executable)
        if not os.path.exists(PROGRAM_PATH):
            answer = True
            if not VERBOSE:
                q = questionary.confirm(_("ask.install", PROGRAM_PATH))
                answer = q.ask()
            if answer:
                os.makedirs(PROGRAM_PATH, exist_ok=True)
                os.makedirs(NODE_PATH, exist_ok=True)
                os.makedirs(PHP_PATH, exist_ok=True)
                os.makedirs(BIN_PATH, exist_ok=True)
                os.makedirs(CACHE_PATH, exist_ok=True)
                download(filename=TO_PATH_PATH,
                         url="https://github.com/Traineratwot/toPath/releases/download/1.2.0/toPath.exe")
                if '.exe' in sys.executable:
                    shutil.copyfile(sys.executable, join(PROGRAM_PATH, "uvm.exe"))
                    addToPath(PROGRAM_PATH)
                return False
        else:
            return True

    @ex(
        help=_("help.base.deInstall"),
    )
    def deInstall(self):
        answer = True
        if not VERBOSE:
            q = questionary.confirm(_("ask.deInstall", ))
            answer = q.ask()
        if answer:
            path_list = os.environ.get('PATH').split(';')
            for path in path_list:
                if PROGRAM_PATH in path:
                    removeToPath(path)
            cmd = f'cmd /c timeout /t 1 & rmdir /s /q "{PROGRAM_PATH}"'
            print(cmd)
            subprocess.Popen(cmd, shell=True)
            exit(0)


class UVM(App):
    class Meta:
        label = 'UVM'
        handlers = [
            Base,
            NodeCli,
            PhpCli,

        ]


if __name__ == '__main__':
    # MAST HAVE
    a1 = cement.ext.ext_dummy
    a2 = cement.ext.ext_smtp
    a3 = cement.ext.ext_plugin
    a4 = cement.ext.ext_configparser
    a5 = cement.ext.ext_logging
    a6 = cement.ext.ext_argparse
    with UVM() as app:
        app.run()
