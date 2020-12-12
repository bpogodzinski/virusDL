import json
import ray

@ray.remote
def host_best(host_sorted_path):
    with open(host_sorted_path) as fd:
        d = json.load(fd)
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

    in_json_path = host_sorted_path
    output_path = in_json_path.parent
    oh = open(output_path.joinpath('hosts_best.json'), 'w')
    json.dump(d1, oh, indent=3)
    oh.close()
    return d1


