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

    host_sorted_info = {
        'is_distance': distance,
        'missing_values': missing_values,
        'best_value_observed': best_value,
        'worst_value_observed': worst_value,
        'null_value': null_value 
    }

    return host_sorted_info
