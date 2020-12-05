import argparse
import json
from pathlib import Path

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import functions
from __CONFIG__ import DATA1_PATH, DATA1_VIRUS_PATH, DATA1_HOST_PATH, RESULTS_PATH


parser = argparse.ArgumentParser(description='Lorem ipsum')
parser.add_argument('-j', '--j', '--json', dest='json', type=argparse.FileType('r'),
                    help='hits_sorted.json', required=True)
parser.add_argument('-t', '--t', '--threshold', dest='threshold', type=float,
                    help='threshold probability', default=0.5)
args = parser.parse_args()


fh = open(DATA1_VIRUS_PATH.joinpath('virus.json'))
dv = json.load(fh)
fh.close()
min_n = len(dv)

fh = open(DATA1_HOST_PATH.joinpath('host.json'))
dh = json.load(fh)
fh.close()

print(len(dv))
print(len(dh))
print(len(dv)* len(dh))


d = json.load(args.json)
args.json.close()

print('Pairs: {}'.format(len(d)))

in_json_path = Path(args.json.name)
output_path = in_json_path.parent


tp_vids = set()
for TAX_RANK in ['species']:
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    for vid, hits in d.items():
        for hit in hits:
            hid = hit[0]
            score = hit[1] 
            match_real = functions.compare(dv[vid], dh[hid], TAX_RANK)
            match_pred = True if score >= args.threshold else False
            if match_pred and match_real:
                tp += 1
                tp_vids.add(vid)
            elif match_pred and not match_real:
                fp += 1
            elif not match_pred and match_real:
                fn += 1
            else:
                tn += 1
    sensitivity = tp/(tp+fn)
    specificity = tn/(tn+fp)
    accuracy = (tp+tn)/(tp+tn+fp+fn)
    d1 = {
        'vids': len(tp_vids),    
        'TP': tp,
        'FP': fp,
        'TN': tn,
        'FN': fn,
        'sensitivity': sensitivity,
        'specificity': specificity,
        'accuracy': accuracy,
    }


    print(TAX_RANK)
    print('vids:        {:,}'.format(len(tp_vids)))
    print('TP:          {:,}'.format(tp))
    print('FP:          {:,}'.format(fp))
    print('TN:          {:,}'.format(tn))
    print('FN:          {:,}'.format(fn))
    print('Sensitivity: {:.3f}'.format(sensitivity))
    print('Specificity: {:.3f}'.format(specificity))
    print('Accuracy:    {:.3f}'.format(accuracy))

oh = open(output_path.joinpath('sens_spec.json'), 'w')
json.dump(d1, oh, indent=3)
oh.close()