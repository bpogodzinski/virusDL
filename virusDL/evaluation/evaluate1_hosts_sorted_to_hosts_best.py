import argparse
import json

from pathlib import Path

import ray

# parser = argparse.ArgumentParser(description='Lorem ipsum')
# parser.add_argument('--json', dest='json', help="json with hits_sorted", type=argparse.FileType('r'), required=True)
# args = parser.parse_args()



# d = json.load(args.json)
# args.json.close()


@ray.remote
def host_best(d):
    d1 = {}
    for vid, hits_lst in d.items():
        d1[vid] = []
        if hits_lst:
            best_score = hits_lst[0][1]
            for hid, score in hits_lst:
                if score == best_score:
                    d1[vid].append([hid, score])
                else:
                    break

    in_json_path = Path(args.json.name)
    output_path = in_json_path.parent
    oh = open(output_path.joinpath('hosts_best.json'), 'w')
    json.dump(d1, oh, indent=3)
    oh.close()

# host_best()



