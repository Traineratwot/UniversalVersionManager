import argparse
from abc import ABC, abstractmethod


class AbstractService(ABC):
    def __init__(self):
        self.setup()

    @abstractmethod
    def use(self, args):
        pass

    @abstractmethod
    def off(self, args):
        pass

    @abstractmethod
    def list(self, args):
        pass

    @abstractmethod
    def install(self, args):
        pass

    @abstractmethod
    def remove(self, args):
        pass

    @abstractmethod
    def path(self, args):
        pass

    @abstractmethod
    def search(self, args):
        pass

    @abstractmethod
    def setup(self):
        pass

    def customCallByName(self, func_name: str, args):
        return 'error'
        pass

    def callByName(self, func_name: str, args):
        match func_name:
            case 'use':
                return self.use(args)
            case 'list':
                return self.list(args)
            case 'install':
                return self.install(args)
            case 'remove':
                return self.remove(args)
            case 'path':
                return self.path(args)
            case 'search':
                return self.search(args)
            case 'off':
                return self.off(args)
            case _:
                return self.customCallByName(func_name, args)
        pass

        pass
