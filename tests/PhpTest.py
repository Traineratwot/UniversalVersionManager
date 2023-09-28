import unittest
from os.path import join, exists

from termcolor import colored

from src.config import PROGRAM_PATH
from src.service.Php import Php


class Args:
    def __init__(self):
        self.version = "5.6.0"


class PhpTest(unittest.TestCase):

    def setUp(self):
        self.args = Args()
        self.php = Php()

    def test_01_node(self):
        print(colored('install', 'green'))
        self.php.install(self.args)
        self.assertTrue(exists(join(PROGRAM_PATH, "php", "5.6.0")))
