import os
import subprocess

from download import download as d

from config import TO_PATH_PATH, SEP, VERBOSE


# import re


def download(url, filename, kind="file"):
    return d(url, filename, progressbar=True, replace=False, kind=kind, verbose=VERBOSE)


def find_max_version(input_string, versions):
    max_version = None
    for version in versions:
        if version.startswith(input_string):
            if max_version is None or version >= max_version:
                max_version = version
    return max_version


def file_put_contents(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


def file_get_contents(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def addToPath(folder: str):
    os.system(f'{TO_PATH_PATH} add "{folder.rstrip(SEP)}"')
    pass


def removeToPath(folder: str):
    os.system(f'{TO_PATH_PATH} remove "{folder.rstrip(SEP)}"')
    pass


def existsToPath(folder: str):
    return os.system(f'{TO_PATH_PATH} exists "{folder.rstrip(SEP)}"') == 0
    pass


def cmd(command, verbose=False):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if verbose:
        print(result.stdout)
    return result.stdout.strip("\n").split('\n') if result.stdout else []


def getVersion(command, verbose=VERBOSE):
    try:
        output = subprocess.check_output(command)
        version = output.decode().strip()
        return version
    except subprocess.CalledProcessError as e:
        if verbose:
            print(f"Ошибка при получении версии Node.js: {e.output.decode().strip()}")
        return None


def createSymlink(source_dir, target_dir, verbose=VERBOSE):
    try:
        os.symlink(source_dir, target_dir)
        if verbose:
            print(f"Symlink created from {source_dir} to {target_dir}")
    except FileExistsError:
        if verbose:
            print(f"Symlink already exists at {target_dir}")
    except OSError as e:
        if verbose:
            print(f"Failed to create symlink: {e}")


def removeSymlink(target_dir, verbose=VERBOSE):
    if os.path.islink(target_dir):
        os.unlink(target_dir)
        if verbose:
            print(f"Symlink {target_dir} success delete.")
    else:
        if verbose:
            print(f"Symlink {target_dir} not exist.")


# def containsNumbers(string):
#     pattern = r'\d+'
#     match = re.search(pattern, string)
#     return bool(match)
