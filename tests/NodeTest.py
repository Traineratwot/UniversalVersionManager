import pprint
import unittest
from os.path import exists, join

from termcolor import colored

from src.config import PROGRAM_PATH, SEP
from src.service import Node
from src.service.Node import getNodeVersions
from src.utils import cmd


class Args:
    def __init__(self):
        self.version = "20.7.0"


class NodeTest(unittest.TestCase):

    def setUp(self):
        self.args = Args()
        self.node = Node.Node()

    def tearDown(self):
        pass

    def test_01_node(self):
        print(colored('install', 'green'))
        self.node.install(self.args)
        self.assertTrue(exists(join(PROGRAM_PATH, "node", "v20.7.0")))

    def test_02_node(self):
        print(colored('use', 'green'))
        self.node.use(self.args)
        self.assertEqual(cmd("node -v")[0], 'v20.7.0')

    def test_03_node(self):
        print(colored('off', 'green'))
        self.node.off(self.args)
        a = len(cmd("node -v"))
        self.assertEqual(a, 0)

    def test_04_node(self):
        print(colored('path', 'green'))
        self.node.remove(self.args)
        self.assertFalse(exists(PROGRAM_PATH + "node" + SEP + "20.7.0"))

    def test_05_getVersions(self):
        v = getNodeVersions()
        pprint.pprint(v)


if __name__ == '__main__':
    unittest.main()
