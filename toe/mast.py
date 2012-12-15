from __future__ import print_function

import json
import requests
from astropy.constants import si


def get_candidates():
    url = u"http://archive.stsci.edu/kepler/candidates/search.php"
    payload = {u"action": u"Search", u"outputformat": u"JSON"}
    r = requests.get(url, params=payload)
    if r.status_code != requests.codes.ok:
        r.raise_for_status()

    candidates = r.json
    for i in range(len(candidates)):
        print(float(i) / len(candidates))
        star = get_star(candidates[i][u"Kepler ID"])[0]
        logg = star[u"Log G (cm/s/s)"]
        if len(logg) == 0:
            continue
        g = 10 ** (float(logg) - 2)
        r = float(star[u"Radius (solar=1.0)"]) * si.R_sun.value
        candidates[i][u"Star Mass"] = g * r * r / si.G.value / si.M_sun.value
        candidates[i][u"Star Radius"] = float(star[u"Radius (solar=1.0)"])

    return candidates


def get_star(sid):
    url = u"http://archive.stsci.edu/kepler/kic10/search.php"
    payload = {u"action": u"Search", u"outputformat": u"JSON",
               u"kic_kepler_id": sid}
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
        candidates = get_candidates()
        for i in range(len(candidates)):
            star = get_star(candidates[i][u"Kepler ID"])[0]
            logg = star[u"Log G (cm/s/s)"]
            if len(logg) == 0:
                print(u"NO")
                continue
            g = 10 ** (float(logg) - 2)
            r = float(star[u"Radius (solar=1.0)"]) * si.R_sun.value
            print(g * r * r / si.G.value / si.M_sun.value)
