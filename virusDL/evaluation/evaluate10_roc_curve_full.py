import json
import pickle
from io import BytesIO

import ray
import matplotlib.pyplot as plt
from sklearn import metrics
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from .__CONFIG__ import DATA1_PATH, DATA1_VIRUS_PATH, DATA1_HOST_PATH

@ray.remote(num_returns=2)
def roc_evaluation(host_sorted, host_sorted_info):
    predictions = {}
    for vid in host_sorted:
        for hid, score in host_sorted[vid]:
            predictions[(vid, hid)] = score

    with open(DATA1_VIRUS_PATH.joinpath('virus.json')) as fh:
        virus_json = json.load(fh)

    with open(DATA1_HOST_PATH.joinpath('host.json')) as fh:
        host_json = json.load(fh)

    with open(DATA1_PATH.joinpath('pairs.p'), 'rb') as fh:
        pairs = pickle.load(fh)

    y = []
    x = []
    for vid in virus_json:
        for hid in host_json:
            pair = (vid, hid)
            label = 1 if pair in pairs['positive'] else 0
            if pair in predictions:
                score = predictions[pair]
                if host_sorted_info['is_distance']:
                    score = host_sorted_info['worst_value_observed'] - score
            else:
                score = host_sorted_info['null_value']
            y.append(label)
            x.append(score)

    fpr, tpr, _ = metrics.roc_curve(y, x)
    roc_auc = metrics.auc(fpr, tpr)
    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.3f' % roc_auc)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    
    plot = BytesIO()
    FigureCanvas(plt).print_png(plot)

    return roc_auc, plot
