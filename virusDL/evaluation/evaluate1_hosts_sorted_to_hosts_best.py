from collections import defaultdict
import ray

@ray.remote(num_cpus=1)
def host_best(host_sorted):
    host_best_result = defaultdict(list)
    for virus_id, hits_list in host_sorted.items():
        best_score = hits_list[0][1]
        for host_id, score in hits_list:
            if score == best_score:
                host_best_result[virus_id].append([host_id, score])
    return host_best_result
