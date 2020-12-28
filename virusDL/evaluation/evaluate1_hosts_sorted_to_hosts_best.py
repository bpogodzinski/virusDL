from collections import defaultdict
import ray

@ray.remote
def filter_best_hosts(host_sorted):
    """Evaluation function that takes sorted results
    and returns best hits

    Args:
        host_sorted (dict): sorted hosts (accuracy) for given virus

    Returns:
        dict: best hosts for given virus
    """
    host_best_result = defaultdict(list)
    for virus_id, hits_list in host_sorted.items():
        best_score = hits_list[0][1]
        for host_id, score in hits_list:
            if score == best_score:
                host_best_result[virus_id].append([host_id, score])
    return host_best_result
