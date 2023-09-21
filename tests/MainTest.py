import os.path
import shutil
import unittest

from config import PROGRAM_PATH
from service import Node
from utils import cmd
from uvm import install


class MyTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists(PROGRAM_PATH):
            shutil.rmtree(PROGRAM_PATH)
        install()

    def tearDown(self):
        if os.path.exists(PROGRAM_PATH):
            shutil.rmtree(PROGRAM_PATH)
        pass

    def test_node(self):
        class Args:
            def __init__(self):
                self.version = "20.7.0"

        args = Args()
        Node.Node().callByName("install", args)
        Node.Node().callByName("use", args)
        self.assertEqual(cmd("node -v")[0], 'v20.7.0')
        Node.Node().callByName("remove", args)
        a = len(cmd("node -v"))
        self.assertEqual(a, 0)


if __name__ == '__main__':
    unittest.main()
