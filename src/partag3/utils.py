import json
import sys

import requests


def get_config(conf_path='./conf.json') -> dict:
    if len(sys.argv) > 1:
        conf_path = sys.argv[1]
        if not conf_path.endswith('.json'):
            conf_path += 'conf.json'

    with open(conf_path) as f:
        return json.loads(f.read())


def load_html(url: str) -> str:
    res = requests.get(url)
    res.raise_for_status()
    return res.text


def track_nat_sort(e):
    digits = '0123456789'
    num = ''
    for sym in e:
        if sym not in digits:
            break
        if sym in digits:
            num += sym
    return int(num)


