from glob import iglob
import json
import pickle
import os

from wirusy.DataLoader import DataLoader

loader = DataLoader('data/')
max_len = 16040666

for train_file in iglob('leave_one_out/**/train.json'):
    dirname = os.path.dirname(train_file)
    print(dirname)
    results_folder = os.path.join(dirname, 'extracted_features')
    os.makedirs(results_folder, exist_ok=True)
    
    with open(train_file, 'r') as f:
        train_dict = json.load(f)
    
    positive_features = []
    negative_features = []

    for positive_pair in train_dict['positive']:
        virus = [record for record in loader.get_fasta(positive_pair[0]) if 'plasmid' not in record.description]
        host = [record for record in loader.get_fasta(positive_pair[1]) if 'plasmid' not in record.description]
        positive_features.append(loader.extract_features(virus, host, max_len))

    for negative_pair in train_dict['negative']:
        virus = [record for record in loader.get_fasta(negative_pair[0]) if 'plasmid' not in record.description]
        host = [record for record in loader.get_fasta(negative_pair[1]) if 'plasmid' not in record.description]
        negative_features.append(loader.extract_features(virus, host, max_len))

    save_dict = {'positive':positive_features, 'negative':negative_features}
    filename = os.path.join(results_folder, 'saved_features.pickle')

    with open(filename, 'wb') as fp:
        pickle.dump(save_dict, fp)

    break

