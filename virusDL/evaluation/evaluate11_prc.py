import ray
import argparse
import json
import pickle
from io import BytesIO

import sklearn.metrics as metrics
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from .__CONFIG__ import DATA1_PATH, DATA1_VIRUS_PATH, DATA1_HOST_PATH

@ray.remote(num_returns=2)
def prc_evaluation(host_sorted, host_sorted_info):
    predictions = {}
    for virus_id in host_sorted:
        for host_id, score in host_sorted[virus_id]:
            predictions[(virus_id, host_id)] = score

    with open(DATA1_VIRUS_PATH.joinpath('virus.json')) as fh:
        virus_json = json.load(fh)

    with open(DATA1_HOST_PATH.joinpath('host.json')) as fh:
        host_json = json.load(fh)

    with open(DATA1_PATH.joinpath('pairs.p'), 'rb') as fh:
        pairs = pickle.load(fh)

    y = []
    x = []
    for virus_id in virus_json:
        for host_id in host_json:
            pair = (virus_id, host_id)
            label = 1 if pair in pairs['positive'] else 0
            if pair in predictions:
                score = predictions[pair]
                if host_sorted_info['is_distance']:
                    score = host_sorted_info['worst_value_observed'] - score
            else:
                score = host_sorted_info['null_value']
            y.append(label)
            x.append(score)


    precision, recall, _ = metrics.precision_recall_curve(y, x)
    prc_auc = metrics.auc(recall, precision)
    plt.title('Precision Recall Curve')

    plt.plot(recall, precision, 'b', label = 'AUC: {:.3}'.format(prc_auc))
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.xlabel('Recall')
    plt.ylabel('Precision')

    plot = BytesIO()
    FigureCanvas(plt).print_png(plot)

    return prc_auc, plot
