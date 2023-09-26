import os
import pprint
import shutil
import unittest

from termcolor import colored

from src.config import PROGRAM_PATH, SEP
from src.service.Php import Php, getPhpVersionFromUserRequest
from uvm import install


class PhpTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists(PROGRAM_PATH):
            shutil.rmtree(PROGRAM_PATH)
        install()

        class Args:
            def __init__(self):
                self.version = "5.6"

        self.args = Args()
        self.php = Php()

    def test_01_node(self):
        print(colored('install', 'green'))
        self.php.callByName("install", self.args)
        self.assertTrue(os.path.exists(PROGRAM_PATH + "php" + SEP + "5.6.9"))

    def test_00_php(self):
        print(colored('test', 'green'))
        versions = getPhpVersionFromUserRequest(self.args)
        pprint.pprint(versions)
