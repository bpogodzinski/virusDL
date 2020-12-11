import argparse
import json
from pathlib import Path

import numpy as np

from __CONFIG__ import DATA1_PATH, DATA1_VIRUS_PATH, DATA1_HOST_PATH, TAXONOMY_RANKS
import functions
import ray

parser = argparse.ArgumentParser(description='')
parser.add_argument('--json', dest='json', help="json with best hits", type=argparse.FileType('r'), required=True)
args = parser.parse_args()


@ray.remote
def run():
    fh = open(DATA1_VIRUS_PATH.joinpath('virus.json'))
    vjson = json.load(fh)
    fh.close()

    fh = open(DATA1_HOST_PATH.joinpath('host.json'))
    hjson = json.load(fh)
    fh.close()

    # Interaction json
    fh = open(DATA1_PATH.joinpath('interactions.json'))
    ijson = json.load(fh)
    fh.close()

    # Taxlevels
    fh = open(DATA1_PATH.joinpath('interactions.taxlevels.json'))
    d = json.load(fh)
    TAX_LEVELS = d['taxlevels']
    fh.close()


    db = json.load(args.json)
    args.json.close()

    d = {}
    for vid, hids in db.items():
        d[vid] = []
        for taxlevel in TAX_LEVELS:
            match = False
            for tup in hids:
                hid = tup[0]
                match = functions.compare(vjson[vid], hjson[hid], taxlevel)
                if match:
                    break
            d[vid].append(match)

    l = [[0, 0] for _i in TAX_LEVELS]
    for vid, imatches in ijson.items():
        for i, taxlevel in enumerate(TAX_LEVELS):
            if imatches[i]:
                l[i][1] += 1
                if d[vid][i]:
                    l[i][0] += 1


    d1 = {}
    i = 0
    for o, e in l:
        d1[TAX_LEVELS[i]] = o/e*100
        i += 1
    in_json_path = Path(args.json.name)
    output_path = in_json_path.parent
    oh = open(output_path.joinpath('performance.json'), 'w')
    json.dump(d1, oh, indent=3)
    oh.close()

run()
