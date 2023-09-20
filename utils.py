from download import download as d


def download(url, filename, kind="file"):
    return d(url, filename, progressbar=True, replace=False, kind=kind, verbose=True)


def find_max_version(input_string, versions):
    max_version = None
    for version in versions:
        if version.startswith(input_string):
            if max_version is None or version >= max_version:
                max_version = version
    return max_version
