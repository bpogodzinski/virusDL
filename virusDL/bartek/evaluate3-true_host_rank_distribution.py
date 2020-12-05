import argparse
import json
from pathlib import Path

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import functions
from __CONFIG__ import DATA1_VIRUS_PATH, DATA1_HOST_PATH, RESULTS_PATH


parser = argparse.ArgumentParser(description='Lorem ipsum')
parser.add_argument('-j', '--j', '--json', dest='json', type=argparse.FileType('r'),
                    help='hits_sorted.json', required=True)
args = parser.parse_args()


fh = open(DATA1_VIRUS_PATH.joinpath('virus.json'))
dv = json.load(fh)
fh.close()

fh = open(DATA1_HOST_PATH.joinpath('host.json'))
dh = json.load(fh)
fh.close()


d = json.load(args.json)
args.json.close()

in_json_path = Path(args.json.name)
output_path = in_json_path.parent

data_to_plot = []
d1 = {}
for TAX_RANK in ['species', 'genus', 'family']:
    L = []
    for vid, hits in d.items():
        l = []
        found = False
        for i, hit in enumerate(hits):
            hid = hit[0] 
            if hid not in l:
                l.append(hid)
                if functions.compare(dv[vid], dh[hid], TAX_RANK):
                    found = True
                    break
        if found:
            L.append(len(l))
    arr = np.array(L)
    d1[TAX_RANK] = {
        'viruses': int(len(arr)),
        'min': int(np.min(arr)),
        'q1': int(np.quantile(arr, 0.25)),
        'q2': int(np.median(arr)),
        'q3': int(np.quantile(arr, 0.75)),
        'max': int(np.max(arr)),
    }
    data_to_plot.append(arr)
    # Create a figure instance
    #fig = plt.figure(1, figsize=(3, 3))
    #num_bins = 100
    #n, bins, patches = plt.hist(arr, num_bins)
    #figure_path = output_path.joinpath('true_host.rank_distibution.{}.svg'.format(TAX_RANK))
    #fig.savefig(figure_path, bbox_inches='tight')   
    #plt.close(fig)

oh = open(output_path.joinpath('true_host.rank_distribution.json'), 'w')
json.dump(d1, oh, indent=3)
oh.close()

# Create a figure instance
fig = plt.figure(1, figsize=(12, 3))

# Create an axes instance
ax = fig.add_subplot(111)

ax.set_xticklabels(['species', 'genus', 'family'])
ax.set_ylabel('rank')
# Create the boxplot
medianprops = dict(linewidth=1, color='black')
bp = ax.boxplot(
    data_to_plot,
    widths=0.6, 
    showfliers=False,
    medianprops=medianprops,
    whiskerprops = dict(linestyle ='--'),
)

# Save the figure
figure_path = output_path.joinpath('true_host.rank_distibution.svg')
fig.savefig(figure_path, bbox_inches='tight')