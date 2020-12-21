import json

from .functions import compare
from .__CONFIG__ import DATA1_VIRUS_PATH, DATA1_HOST_PATH
import ray

@ray.remote
def evaluate_binary_classification(host_sorted, threshold = 0.5):

    with open(DATA1_VIRUS_PATH.joinpath('virus.json')) as fh:
        virus_json = json.load(fh)

    with open(DATA1_HOST_PATH.joinpath('host.json')) as fh:
        host_json = json.load(fh)

    result_stats = {}
    true_positive_virus_ids = set()
    for TAX_RANK in ['species']:
        true_positive = 0
        false_positive = 0
        false_negative = 0
        true_negative = 0

        for virus_id, hits in host_sorted.items():
            for hit in hits:
                host_id = hit[0]
                score = hit[1] 
                match_real = compare(virus_json[virus_id], host_json[host_id], TAX_RANK)
                match_pred = True if score >= threshold else False
                if match_pred and match_real:
                    true_positive += 1
                    true_positive_virus_ids.add(virus_id)
                elif match_pred and not match_real:
                    false_positive += 1
                elif not match_pred and match_real:
                    false_negative += 1
                else:
                    true_negative += 1

        sensitivity = true_positive/(true_positive+false_negative)
        specificity = true_negative/(true_negative+false_positive)
        accuracy = (true_positive+true_negative)/(true_positive+true_negative+false_positive+false_negative)
        result_stats = {
            'vids': len(true_positive_virus_ids),    
            'TP': true_positive,
            'FP': false_positive,
            'TN': true_negative,
            'FN': false_negative,
            'sensitivity': sensitivity,
            'specificity': specificity,
            'accuracy': accuracy,
        }

    return result_stats
