import os.path
import shutil
import unittest

from termcolor import colored

from config import PROGRAM_PATH, SEP
from service import Node
from service.Node import getVersions
from utils import cmd
from uvm import install


class NodeTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists(PROGRAM_PATH):
            shutil.rmtree(PROGRAM_PATH)
        install()

        class Args:
            def __init__(self):
                self.version = "20.7.0"

        self.args = Args()
        self.node = Node.Node()

    def tearDown(self):
        if os.path.exists(PROGRAM_PATH):
            shutil.rmtree(PROGRAM_PATH)
        pass

    def test_01_node(self):
        print(colored('install', 'green'))
        self.node.callByName("install", self.args)
        self.assertTrue(os.path.exists(PROGRAM_PATH + "node" + SEP + "20.7.0"))

    def test_02_node(self):
        print(colored('use', 'green'))
        self.node.callByName("use", self.args)
        self.assertEqual(cmd("node -v")[0], 'v20.7.0')

    def test_03_node(self):
        print(colored('off', 'green'))
        self.node.callByName("off", self.args)
        a = len(cmd("node -v"))
        self.assertEqual(a, 0)

    def test_04_node(self):
        print(colored('path', 'green'))
        self.node.callByName("remove", self.args)
        self.assertFalse(os.path.exists(PROGRAM_PATH + "node" + SEP + "20.7.0"))

    def test_05_getVerions(self):
        v = getVersions()
        print(v)


if __name__ == '__main__':
    unittest.main()
