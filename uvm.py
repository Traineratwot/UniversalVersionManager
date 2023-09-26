import os

from cement import App

from src.cli.nodeCli import NodeCli
from src.cli.phpСli import PhpCli
from src.config import PROGRAM_PATH, NODE_PATH, PHP_PATH, BIN_PATH, CACHE_PATH, TO_PATH_PATH
from src.utils import download


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
    if not os.path.exists(PROGRAM_PATH):
        install()
    with UVM() as app:
        app.run()
