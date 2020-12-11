import ray
import argparse
import json
from pathlib import Path
import pickle
import numpy as np

import sklearn.metrics as metrics
import matplotlib.pyplot as plt

from __CONFIG__ import DATA1_PATH, DATA1_VIRUS_PATH, DATA1_HOST_PATH

parser = argparse.ArgumentParser(description='Lorem ipsum')
parser.add_argument('-d', '--d', '--dir', dest='dir', help="dir to hosts_best.json", required=True)
args = parser.parse_args()


@ray.remote()
def run():
    dir_path = Path(args.dir)
    fh = open(dir_path.joinpath('hosts_sorted.json'))
    d = json.load(fh)
    dpred = {}
    for vid in d:
        for hid, score in d[vid]:
            dpred[(vid, hid)] = score
    fh.close()

    fh = open(DATA1_VIRUS_PATH.joinpath('virus.json'))
    vjson = json.load(fh)
    fh.close()

    fh = open(DATA1_HOST_PATH.joinpath('host.json'))
    hjson = json.load(fh)
    fh.close()

    fh = open(DATA1_PATH.joinpath('pairs.p'), 'rb')
    pairs = pickle.load(fh)
    fh.close()


    fh = open(dir_path.joinpath('hosts_sorted.info.json'))
    info = json.load(fh)
    fh.close()

    y = []
    x = []
    for vid in vjson:
        for hid in hjson:
            pair = (vid, hid)
            label = 1 if pair in pairs['positive'] else 0
            if pair in dpred:
                score = dpred[pair]
                if info['is_distance']:
                    score = info['worst_value_observed'] - score
            else:
                score = info['null_value']
            y.append(label)
            x.append(score)


    precision, recall, threshold = metrics.precision_recall_curve(y, x)
    auc = metrics.auc(recall, precision)
    plt.title('Precision Recall Curve')

    plt.plot(recall, precision, 'b', label = 'AUC: {:.3}'.format(auc))
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.savefig(dir_path.joinpath('prc_full.png'))


    oh = open(dir_path.joinpath('auc_prc.txt'), 'w')
    oh.write('{:.3f}'.format(auc))
    oh.close()

run()
