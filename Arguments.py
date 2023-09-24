import argparse


class Arguments:
    version = ""
    action = ""
    service = ""

    def __init__(self, args: argparse.Namespace):
        self.version = args.version
        self.action = args.action
        self.service = args.service
