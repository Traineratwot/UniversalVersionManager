import re
from os.path import join, dirname

regex = r"UVM_VERSION = r'(\d+)\.(\d+)\.(\d+)'"


def file_put_contents(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


def file_get_contents(file_path):
    with open(file_path, 'r') as file:
        return file.read()


try:
    path = join(dirname(dirname(__file__)), "version.py")
    text = file_get_contents(path)
    matches = re.search(regex, text)
    if matches:
        groups = matches.groups()
        Major = int(groups[0])
        Minor = int(groups[0])
        Build = int(groups[2]) + 1
        text = f"UVM_VERSION = r'{Major}.{Minor}.{Build}'"
        file_put_contents(path, text)
except ValueError:
    pass
