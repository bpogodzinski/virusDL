import argparse
from collections import defaultdict
import json
from pathlib import Path

import numpy as np

from .__CONFIG__ import DATA1_PATH, DATA1_VIRUS_PATH, DATA1_HOST_PATH, TAXONOMY_RANKS
from .functions import compare
import ray


@ray.remote
def evaluate_taxonomy_performance(best_hosts):
    with open(DATA1_VIRUS_PATH.joinpath('virus.json')) as fd:
        virus_json = json.load(fd)

    with open(DATA1_HOST_PATH.joinpath('host.json')) as fd:
        host_json = json.load(fd)

    with open('/home/panda/workspace/wirusy/virusDL/evaluation/interactions.json') as fd:
        interaction_json = json.load(fd)

    TAX_LEVELS = TAXONOMY_RANKS[::-1]

    d = defaultdict(list)
    for virus_id, hosts in best_hosts.items():
        for taxlevel in TAX_LEVELS:
            match = False
            for entry in hosts:
                host_id = entry[0]
                match = compare(virus_json[virus_id], host_json[host_id], taxlevel)
                if match:
                    break
            d[virus_id].append(match)

    l = [[0, 0] for _i in TAX_LEVELS]
    for virus_id, imatches in interaction_json.items():
        for i, taxlevel in enumerate(TAX_LEVELS):
            if imatches[i]:
                l[i][1] += 1
                if d[virus_id][i]:
                    l[i][0] += 1


    d1 = {}
    i = 0
    for o, e in l:
        d1[TAX_LEVELS[i]] = o/e*100
        i += 1

    return d1