import json
from io import BytesIO

import ray
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from .functions import compare
from .__CONFIG__ import DATA1_VIRUS_PATH, DATA1_HOST_PATH


@ray.remote(num_returns=2)
def true_host_rank_distribution(host_sorted):
    with open(DATA1_VIRUS_PATH.joinpath('virus.json')) as fd:
        virus_json = json.load(fd)

    with open(DATA1_HOST_PATH.joinpath('host.json')) as fd:
        host_json = json.load(fd)

    data_to_plot = []
    host_rank_distribution = {}
    for TAX_RANK in ['species', 'genus', 'family']:
        L = []
        for virus_id, hosts in host_sorted.items():
            host_ids = []
            found = False
            for host in hosts:
                host_id = host[0] 
                if host_id not in host_ids:
                    host_ids.append(host_id)
                    if compare(virus_json[virus_id], host_json[host_id], TAX_RANK):
                        found = True
                        break
            if found:
                L.append(len(host_ids))
        arr = np.array(L)
        host_rank_distribution[TAX_RANK] = {
            'viruses': int(len(arr)),
            'min': int(np.min(arr)),
            'q1': int(np.quantile(arr, 0.25)),
            'q2': int(np.median(arr)),
            'q3': int(np.quantile(arr, 0.75)),
            'max': int(np.max(arr)),
        }
        data_to_plot.append(arr)

    # Create the boxplot
    fig = plt.figure(1, figsize=(12, 3))
    ax = fig.add_subplot(111)
    ax.set_xticklabels(['species', 'genus', 'family'])
    ax.set_ylabel('rank')
    medianprops = dict(linewidth=1, color='black')
    ax.boxplot(
        data_to_plot,
        widths=0.6, 
        showfliers=False,
        medianprops=medianprops,
        whiskerprops = dict(linestyle ='--'),
    )

    # Save the figure in memory
    plot = BytesIO()
    FigureCanvas(fig).print_png(plot)

    return host_rank_distribution, plot
