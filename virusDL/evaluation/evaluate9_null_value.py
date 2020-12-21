import ray

@ray.remote
def evaluate_sorted_hosts(host_sorted):

    # Check whether values are scores or distance
    distance = True
    for hits in host_sorted.values():
        values = [score for _, score in hits]
        if len(values) > 1:
            if values[0] < values[-1]:
                break
            elif values[0] > values[-1]:
                distance = False
                break

    lst = [score for hits in host_sorted.values() for _, score in hits]
    missing_values = 20897286 - len(lst)

    min_val = min(lst)
    max_val = max(lst)

    best_value = min_val if distance else max_val 
    worst_value = max_val if distance else min_val
    null_value = max_val if distance else 0.0

    # TODO: Check this output path
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

    host_sorted_info = {
        'is_distance': distance,
        'missing_values': missing_values,
        'best_value_observed': best_value,
        'worst_value_observed': worst_value,
        'null_value': null_value 
    }

    return host_sorted_info
