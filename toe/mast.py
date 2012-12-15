from __future__ import print_function

import json
import requests


url = u"http://archive.stsci.edu/kepler/candidates/search.php"


def get_candidates():
    payload = {u"action": u"Search", u"outputformat": u"JSON"}
    r = requests.get(url, params=payload)
    if r.status_code != requests.codes.ok:
        r.raise_for_status()

    return r.json


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        json.dump(get_candidates(), open(sys.argv[1], u"w"),
                  indent=4, separators=(',', ': '))
    else:
        print(get_candidates())
