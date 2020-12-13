from pathlib import Path
import ray
import json
from evaluation.evaluate1_hosts_sorted_to_hosts_best import host_best

ray.init(num_cpus=2)
host_sorted = None

with open(Path('/home/panda/workspace/wirusy/whole.json')) as fd:
    host_sorted = json.load(fd)


# ściągamy wszystkie pliki evaluacji, robimy graf\
best_hosts = host_best.remote(host_sorted)


result = ray.get(best_hosts)
# odpalamy każdy z zadanymi parametrami w linii kommend input output path 

# do jednego katalogu results z datą

ray.shutdown()