from src.service.Php import getPhpVersionFromUserRequest


class Args:
    def __init__(self):
        self.version = "5"


args = Args()

print(getPhpVersionFromUserRequest(args))
