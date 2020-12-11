import argparse
import json
from pathlib import Path

import ray



parser = argparse.ArgumentParser(description='Lorem ipsum')
parser.add_argument('-j', '--j', '--json', dest='json', type=argparse.FileType('r'),
                    help='hits_sorted.json', required=True)
args = parser.parse_args()


@ray.remote
def run():
    d = json.load(args.json)
    args.json.close()


    in_json_path = Path(args.json.name)
    output_path = in_json_path.parent


    # Check whether values are scores or distance
    distance = True
    for vid, hits in d.items():
        values = [score for hid, score in hits]
        if len(values) > 1:
            if values[0] < values[-1]:
                break
            elif values[0] > values[-1]:
                distance = False
                break


    lst = [score for vid, hits in d.items() for hid, score in hits]
    missing_values = 20897286 - len(lst)

    min_val = min(lst)
    max_val = max(lst)

    best_value = min_val if distance else max_val 
    worst_value = max_val if distance else min_val
    null_value = max_val if distance else 0.0

    run_name = str(output_path)
    if 'pvalue' in run_name:
        null_value = 1.0
    if 'mash' in run_name:
        null_value = 1.0
    if 'correlation_kendalltau' in run_name:
        null_value = 2.0
    if 'correlation_pearson' in run_name:
        null_value = 2.0
    if 'google' in run_name:
        null_value = 1.0
    if 'gc_content' in run_name:
        null_value = 1.0
    if 'mean_normalization' in run_name:
        null_value = -1.0
    if 'dna2vec' in run_name:
        null_value = 1.0
    if 'pearsonr' in run_name:
        null_value = -1.0
    if 'cosine' in run_name:
        null_value = 1.0
    if '-kendalltau' in run_name:
        null_value = -1.0
    if 'wish' in run_name:
        null_value = worst_value

    d = {
        'is_distance': distance,
        'missing_values': missing_values,
        'best_value_observed': best_value,
        'worst_value_observed': worst_value,
        'null_value': null_value 
    }


    oh = open(output_path.joinpath('hosts_sorted.info.json'), 'w')
    json.dump(d, oh, indent=3)
    oh.close()

run()
