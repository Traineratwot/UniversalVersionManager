import os
import subprocess
import sys

import cement.ext.ext_argparse
import cement.ext.ext_configparser
import cement.ext.ext_dummy
import cement.ext.ext_logging
import cement.ext.ext_plugin
import cement.ext.ext_smtp
import questionary
import requests
from cement import App, ex, Controller

from src.cli.nodeCli import NodeCli
from src.cli.phpСli import PhpCli
from src.config import PROGRAM_PATH, VERBOSE
from src.lang import _
from src.stat import sendStat, futures
from src.utils import removeToPath, install
from version import UVM_VERSION


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
        install()

    @ex(
        label="uninstall",
        help=_("help.base.deInstall"),
    )
    def deInstall(self):
        sendStat('uninstall')
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

    @ex(
        aliases=['v'],
        label="version",
        help=_("help.base.printVersion", UVM_VERSION),
    )
    def printVersion(self):
        print(UVM_VERSION)


class UVM(App):
    class Meta:
        label = 'UVM'
        handlers = [
            Base,
            NodeCli,
            PhpCli,

        ]


if __name__ == '__main__':
    try:
        # MAST HAVE
        a1 = cement.ext.ext_dummy
        a2 = cement.ext.ext_smtp
        a3 = cement.ext.ext_plugin
        a4 = cement.ext.ext_configparser
        a5 = cement.ext.ext_logging
        a6 = cement.ext.ext_argparse
        a7 = UVM_VERSION
        with UVM() as app:
            app.run()
        for future in futures:
            future.get()
    except requests.exceptions.HTTPError:
        pass
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.RequestException:
        pass
    except ValueError as e:
        print("Error")
        print(e)
        pass
