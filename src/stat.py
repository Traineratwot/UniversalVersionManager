import getpass
import hashlib
import json
import sys
from multiprocessing.dummy import Pool
from urllib.parse import urljoin, urlencode
from uuid import getnode as get_mac

import requests
from SimpleCache2 import simple_cache

from lang import langKey
from src.cache import MEMORY

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
    try:
        futures.append(pool.apply_async(send, args=[action, data]))
    except ValueError:
        pass
    pass


def send(action: str = None, data: dict = None) -> None:
    userId = getUserId()
    url = r'https://unicorn.traineratwot.site/matomo.php?'
    argv = sys.argv.pop(0)
    params = {
        "apiv": "1",
        "idsite": "4",
        "rec": "1",
        "ua": "UVM",
        "url": urljoin('', argv)
    }
    if action:
        params['action_name'] = action
    if data:
        params['uadata'] = json.dumps(data)
    if userId:
        params['_id'] = userId
    if langKey:
        params['lang'] = langKey
    url = url + urlencode(params)
    try:
        requests.request("GET", url, timeout=5)
    except requests.exceptions.HTTPError:
        pass
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.RequestException:
        pass
    pass
