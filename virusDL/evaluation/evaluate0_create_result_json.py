import json
import ray

@ray.remote
def concat_and_sort_results(tests_folder):
    """Concatenate and sort results

    Args:
        tests_folder (Path): Path to folder with tests

    Returns:
        dict: sorted hosts for given virus
    """
    results = tests_folder.rglob('results.json')
    host_sorted = {}

    for file in results:
        with open(file) as fd:
            host_sorted.update(json.load(fd))
    for hits_list in host_sorted.values():
        hits_list.sort(key=lambda x: x[1], reverse=True)

    return host_sorted 