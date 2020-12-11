import ray
import json
from evaluation.evaluate1_hosts_sorted_to_hosts_best import host_best

ray.init()
host_sort = json.load(open('/home/panda/workspace/wirusy/whole.json'))
# ściągamy wszystkie pliki evaluacji, robimy graf

best = host_best.remote(host_sort)

result = ray.get(best)
# odpalamy każdy z zadanymi parametrami w linii kommend input output path 

# do jednego katalogu results z datą
