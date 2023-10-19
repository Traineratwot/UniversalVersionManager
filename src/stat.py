import getpass
import hashlib
import json
import sys
from multiprocessing.dummy import Pool
from urllib.parse import urljoin, urlencode
from uuid import getnode as get_mac

import requests
from SimpleCache2 import simple_cache

from src.cache import MEMORY
from src.lang import langKey
from version import UVM_VERSION

pool = Pool(10)
futures = []


@simple_cache(MEMORY)
def md5(string: str) -> str:
    h = hashlib.new('md5')
    h.update(string.encode('utf-8'))
    return h.hexdigest()
    pass


@simple_cache(MEMORY)
def getUserId() -> str:
    mac = get_mac()
    name = getpass.getuser()
    uuid = md5(fr"{name}-{mac}")
    return uuid
    pass


def sendStat(action: str = None, data: dict = None) -> None:
    # send(action,data)
    try:
        futures.append(pool.apply_async(send, args=[action, data]))
    except ValueError:
        pass
    pass


def send(action: str = None, data: dict = None) -> None:
    userId = getUserId()
    url = r'https://thor.traineratwot.site/api/event'
    sys.argv.pop(0)
    payload = {
        "domain": "uvm",
        "url": "/".join(sys.argv),
    }
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/'+UVM_VERSION,
        'X-Forwarded-For': userId,
    }

    if action:
        payload['name'] = action
    if data:
        payload['props'] = json.dumps(data)
    try:
        requests.request("POST", url, headers=headers, data=json.dumps(payload), timeout=2, verify=False)
    except requests.exceptions.HTTPError:
        pass
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.RequestException:
        pass
    pass
