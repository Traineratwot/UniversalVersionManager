import sys
from urllib.parse import urljoin
argv = sys.argv.pop(0)
print(urljoin('', argv))
