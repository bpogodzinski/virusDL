from pathlib import Path
from io import BytesIO

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import ray

@ray.remote(num_returns=2)
def positive_negative_scores_distribution(host_sorted):
    pairs = {}
    for pair_type in ['positive', 'negative']:
        pairs[pair_type] = set([])
        fh = open(Path(f'/home/panda/workspace/wirusy/data/{pair_type}_pairs.csv'))
        fh.readline()
        for line in fh:
            sl = line.strip().split(',')
            vid = sl[0]
            hid = sl[1]
            pairs[pair_type].add((vid, hid))
        fh.close()


    positive_scores = []
    negative_scores = []
    for vid in host_sorted:
        for hid, score in host_sorted[vid]:
            tup = (vid, hid)
            if tup in pairs['positive']:
                positive_scores.append(score)
            elif tup in pairs['negative']:
                negative_scores.append(score)

    scores_distribution = {}
    for label, lst in [('positive', positive_scores), ('negative', negative_scores)]:
        array = np.array(lst)
        q1 = np.quantile(array, 0.25)
        q2 = np.median(array)
        q3 = np.quantile(array, 0.75)

        scores_distribution[label] = {
          'min': float(np.min(array)),
          'q1': float(q1),
          'q2': float(q2),
          'q3': float(q3),
          'max': float(np.max(array))
        }

    data_to_plot = [positive_scores, negative_scores]

    fig = plt.figure(1, figsize=(3, 3))
    ax = fig.add_subplot(111)
    ax.set_xticklabels(['positive', 'negative'])
    ax.set_ylabel('score')
    medianprops = dict(linewidth=1, color='black')
    bp = ax.boxplot(
        data_to_plot,
        widths=0.6, 
        showfliers=False,
        medianprops=medianprops,
        whiskerprops = dict(linestyle ='--'),

    )
    # res  = {}
    # for key, value in bp.items():
    #     res[key] = [v.get_data() for v in value]

    # Save the figure in memory
    plot = BytesIO()
    FigureCanvas(fig).print_png(plot)

    return scores_distribution, plot