from pathlib import Path
import ray
import json
from evaluation.evaluate0_create_result_json import concat_and_sort_results
from evaluation.evaluate1_hosts_sorted_to_hosts_best import filter_best_hosts
from evaluation.evaluate2_hits_best_json import evaluate_taxonomy_performance

ray.init(num_cpus=2)
tests_folder = Path('/home/panda/workspace/wirusy/tests')

# ściągamy wszystkie pliki evaluacji, robimy graf
host_sorted = concat_and_sort_results.remote(tests_folder)
best_hosts = filter_best_hosts.remote(host_sorted)
tax_performance = evaluate_taxonomy_performance.remote(best_hosts)

result = ray.get(tax_performance)

# do jednego katalogu results z datą

ray.shutdown() 