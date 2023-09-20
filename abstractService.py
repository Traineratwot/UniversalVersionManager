import argparse
from abc import ABC, abstractmethod


class abstractService(ABC):
    @abstractmethod
    def use(self, args: argparse.Namespace):
        pass

    @abstractmethod
    def list(self, args: argparse.Namespace):
        pass

    @abstractmethod
    def install(self, args: argparse.Namespace):
        pass

    @abstractmethod
    def remove(self, args: argparse.Namespace):
        pass

    @abstractmethod
    def path(self, args: argparse.Namespace):
        pass

    @abstractmethod
    def search(self, args: argparse.Namespace):
        pass

    def callByName(self, func_name, args: argparse.Namespace):
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
            case _:
                print("Изи на хуй придурок")
        pass

        pass
