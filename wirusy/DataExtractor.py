import logging
from multiprocessing import process
import multiprocessing
import os
import pickle
import json
from pathlib import Path
import numpy as np

from Bio import SeqIO


class DataExtractor:
    def __init__(self, data_folder, tests_folder, feature_list=None):
        with open(os.path.join(data_folder, "virus", "virus.json")) as f:
            self.virus_json = json.load(f)
        with open(os.path.join(data_folder, "host", "host.json")) as f:
            self.host_json = json.load(f)
        with open(os.path.join(data_folder, "features.index.json")) as f:
            self.features_json = json.load(f)
        with open(os.path.join(data_folder, "vh.index.p"), "rb") as f:
            self.features_index = pickle.load(f)
        self.virus_fasta_folder = Path(os.path.join(data_folder, "virus", "fasta"))
        self.host_fasta_folder = Path(os.path.join(data_folder, "host", "fasta"))
        self.features_folder = Path(os.path.join(data_folder, "features"))
        self.tests_folder = Path(tests_folder)
        self.feature_list = feature_list if feature_list else None
        self.feature_data_map = self.__load_feature_data(feature_list) if feature_list else None

    def get_fasta(self, ncbi_id):
        if ncbi_id in self.virus_json:
            return SeqIO.parse(self.virus_fasta_folder / ncbi_id / ".fna", "fasta")
        elif ncbi_id in self.host_json:
            return SeqIO.parse(self.host_fasta_folder / ncbi_id / ".fna", "fasta")
        else:
            raise LookupError(f"Can't find {ncbi_id} in virus or host json file")

    def get_features(self, virus, host):
        assert self.feature_list, "Feature list not provided!"
        index = self.features_index[(virus, host)]
        x = np.array([self.feature_data_map[feature][index] for feature in self.feature_list])
        return x

    def extract_features_from_test_folder(self, test_folder, check_existing_file = True, save_to_file=False, filename="X_Y.p"):
        TRAIN_JSON = "train.json"
        TEST_JSON = "test.json"

        process_info = multiprocessing.current_process().name
        x_train = []
        y_train = []

        if check_existing_file and (test_folder / filename).exists():
            logging.info(
                f"Worker {process_info} skipping {test_folder / filename}, file exists! Returning data from file."
            )
            return pickle.load(open(test_folder / filename, "rb"))

        with open(test_folder / TRAIN_JSON) as fd:
            train_data = json.load(fd)
            train_positive = train_data["positive"]
            train_negative = train_data["negative"]
            len_positive = len(train_positive)
            len_all = len_positive + len(train_negative)

            for index, positive in enumerate(train_positive, start=1):
                logging.info(f"Worker {process_info} doing positive {positive} from {test_folder} {index}/{len_all}")
                virus_id = positive[0]
                host_id = positive[1]
                x = self.get_features(virus_id, host_id)
                x_train.append(x)
                y_train.append(1)

            for index, negative in enumerate(train_negative, start=1):
                logging.info(
                    f"Worker {process_info} doing negative {negative} from {test_folder} {index + len_positive}/{len_all}"
                )
                virus_id = negative[0]
                host_id = negative[1]
                x = self.get_features(virus_id, host_id)
                x_train.append(x)
                y_train.append(0)

        X, Y = np.array(x_train), np.array(y_train)

        if save_to_file:
            with open(test_folder / filename, "wb") as fd:
                pickle.dump([X, Y], fd)
                logging.info(f"Worker {process_info} saved file {filename} in {test_folder}")

        return X, Y

    def __load_feature_data(self, feature_list):
        return {
            feature: pickle.load(open((self.features_folder / self.features_json[feature]["file"]), "rb"))
            for feature in feature_list
        }
