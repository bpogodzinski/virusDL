import argparse
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import functions
from __CONFIG__ import DATA1_PATH, RESULTS_PATH
import ray


parser = argparse.ArgumentParser(description='Lorem ipsum')
parser.add_argument('-j', '--j', '--json', dest='json', type=argparse.FileType('r'),
                    help='hits_sorted.json', required=True)
args = parser.parse_args()

d = json.load(args.json)
args.json.close()


@ray.remote
def run():
    pairs = {}
    for pair_type in ['positive', 'negative']:
        pairs[pair_type] = set([])
        fh = open(DATA1_PATH.joinpath('{}_pairs.csv'.format(pair_type)))
        fh.readline()
        for line in fh:
            sl = line.strip().split(',')
            vid = sl[0]
            hid = sl[1]
            pairs[pair_type].add((vid, hid))
        fh.close()


    positive_scores = []
    negative_scores = []
    for vid in d:
        for hid, score in d[vid]:
            tup = (vid, hid)
            if tup in pairs['positive']:
                positive_scores.append(score)
            elif tup in pairs['negative']:
                negative_scores.append(score)




    in_json_path = Path(args.json.name)
    output_path = in_json_path.parent
    d1 = {}
    for label, lst in [('positive', positive_scores), ('negative', negative_scores)]:
        array = np.array(lst)
        q1 = np.quantile(array, 0.25)
        q2 = np.median(array)
        q3 = np.quantile(array, 0.75)

        d1[label] = {
          'min': float(np.min(array)),
          'q1': float(q1),
          'q2': float(q2),
          'q3': float(q3),
          'max': float(np.max(array))
        }

    oh = open(output_path.joinpath('positive_negative.scores-distribution.json'), 'w')
    json.dump(d1, oh, indent=3)
    oh.close()


    data_to_plot = [positive_scores, negative_scores]
    # Create a figure instance
    fig = plt.figure(1, figsize=(3, 3))

    # Create an axes instance
    ax = fig.add_subplot(111)

    ax.set_xticklabels(['positive', 'negative'])
    ax.set_ylabel('score')
    # Create the boxplot
    medianprops = dict(linewidth=1, color='black')
    bp = ax.boxplot(
        data_to_plot,
        widths=0.6, 
        showfliers=False,
        medianprops=medianprops,
        whiskerprops = dict(linestyle ='--'),

    )
    res  = {}
    for key, value in bp.items():
        res[key] = [v.get_data() for v in value]

    # Save the figure
    figure_path = output_path.joinpath('positive_negative.scores-boxplot.svg')
    fig.savefig(figure_path, bbox_inches='tight')

run()
