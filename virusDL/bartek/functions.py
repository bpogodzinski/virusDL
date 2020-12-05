import itertools
import random


def compare(vd, hd, rank):
    vi = vd['host']['lineage_ranks'].index(rank) if rank in vd['host']['lineage_ranks'] else None
    hi = hd['lineage_ranks'].index(rank) if rank in hd['lineage_ranks'] else None
    if vi != None and hi != None:
        if vd['host']['lineage_names'][vi] == hd['lineage_names'][hi]:
            return True
    return False


def reverse_complement(seq):
    d = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return "".join([d.get(nt, 'N') for nt in seq[::-1]])


def list_canonical_kmers(k=6):
    """Create a sorted list of canonical k-mers of a given length (k).

    Args:
        k (int) : k-mer length

    Example:
        >>> l = list_canonical_kmers(k=2)
        ['AA', 'AC', 'AG', 'AT', 'CA', 'CC', 'CG', 'GA', 'GC', 'TA']   
    """    
    s = set()
    for tup in itertools.product(['A', 'C', 'G', 'T'], repeat=k):
        kmer = "".join(tup)
        kmer_canonical = sorted([kmer, reverse_complement(kmer)])[0]
        s.add(kmer_canonical)
    return sorted(list(s))


def rank_to_name(d, rank):
    name = None
    if rank in d['lineage_ranks']:
        idx = d['lineage_ranks'].index(rank)
        name = d['lineage_names'][idx]
    return name



def diffranks_at_samerank(vd, hd, vid, hids, diff_rank, same_rank=None):
    d = {}
    random.shuffle(hids)

    vdiff_name = rank_to_name(vd[vid]['host'], diff_rank)
    if not vdiff_name:
        return d

    if not same_rank:
        for hid in hids:
            hdiff_name = rank_to_name(hd[hid], diff_rank)
            if hdiff_name and hdiff_name != vdiff_name:
                if hdiff_name not in d:
                    d[hdiff_name] = []
                d[hdiff_name].append(hid)
    else:
        vsame_name = rank_to_name(vd[vid]['host'], same_rank)
        if not vsame_name:
            return d
        for hid in hids:
            hsame_name = rank_to_name(hd[hid], same_rank)
            hdiff_name = rank_to_name(hd[hid], diff_rank)
            if hsame_name and vsame_name == hsame_name:
                if hdiff_name and vdiff_name != hdiff_name:
                    if hdiff_name not in d:
                        d[hdiff_name] = []
                    d[hdiff_name].append(hid)
    return d


def choose_one(d):
    groups = list(d.values())
    one = None
    if groups:
        group_idx = random.randint(0, len(groups)-1)
        one = random.choice(groups[group_idx])
    return one


def choose_n(d, n):
    l = []
    pool_n = len([el for taxrank in d for el in d[taxrank]])
    groups = list(d.values())
    random.shuffle(groups)
    threshold_n = min([pool_n, n])
    i = 0
    while len(l) < threshold_n:
        if i == len(groups):
            i = 0
        # Skip group if empty
        if groups[i]:
            choice = random.choice(groups[i])
            l.append(choice)
            groups[i].remove(choice)
        i += 1
    return l




if __name__ == '__main__':
    import json
    from __CONFIG__ import DATA1_VIRUS_PATH, DATA1_HOST_PATH

    fh = open(DATA1_VIRUS_PATH.joinpath('virus.json'))
    vd = json.load(fh)
    fh.close()

    fh = open(DATA1_HOST_PATH.joinpath('host.json'))
    hd = json.load(fh)
    fh.close()

    vid = 'NC_025830'
    hids = list(hd.keys())
    d = diffranks_at_samerank(vd, hd, vid, hids, 'family', 'order')
    for taxrank in d:
        for hid in d[taxrank]:
            same_match = compare(vd[vid], hd[hid], 'order')
            diff_match = compare(vd[vid], hd[hid], 'family')
            if not same_match or diff_match:
                print('NOT OK: {}-{}'.format(vid, hid, 'family', 'order'))        
    d = diffranks_at_samerank(vd, hd, vid, hids, 'superkingdom', None)
    for taxrank in d:
        for hid in d[taxrank]:
            diff_match = compare(vd[vid], hd[hid], 'superkingdom')
            if diff_match:
                print('NOT OK: {}-{}'.format(vid, hid, 'family', 'order'))    
