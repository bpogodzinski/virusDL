import argparse
import json
import pickle
from pathlib import Path

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from sklearn import metrics

import functions
from __CONFIG__ import DATA1_PATH, DATA1_VIRUS_PATH, DATA1_HOST_PATH


parser = argparse.ArgumentParser(description='Lorem ipsum')
parser.add_argument('-j', '--j', '--json', dest='json', type=argparse.FileType('r'),
                    help='hits_sorted.json', required=True)
args = parser.parse_args()


d = json.load(args.json)
args.json.close()
dpred = {}
for vid in d:
    for hid, score in d[vid]:
        dpred[(vid, hid)] = score

in_json_path = Path(args.json.name)
output_path = in_json_path.parent


fh = open(DATA1_VIRUS_PATH.joinpath('virus.json'))
vjson = json.load(fh)
fh.close()


fh = open(DATA1_HOST_PATH.joinpath('host.json'))
hjson = json.load(fh)
fh.close()

fh = open(DATA1_PATH.joinpath('pairs.p'), 'rb')
pairs = pickle.load(fh)
fh.close()


fh = open(output_path.joinpath('hosts_sorted.info.json'))
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


fpr, tpr, threshold = metrics.roc_curve(y, x)
roc_auc = metrics.auc(fpr, tpr)
plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b', label = 'AUC = %0.3f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.savefig(output_path.joinpath('roc_full.png'))



oh = open(output_path.joinpath('auc_full.txt'), 'w')
oh.write('{:.3f}'.format(roc_auc))
oh.close()
