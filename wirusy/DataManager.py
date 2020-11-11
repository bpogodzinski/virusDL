import logging
import multiprocessing
import os
import pickle
import json
from pathlib import Path
from functools import partial

import numpy as np

from Bio import SeqIO

class DataManager:
    def __init__(self, data_folder, tests_folder):
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

    def get_fasta(self, ncbi_id):
        if ncbi_id in self.virus_json:
            return SeqIO.parse(self.virus_fasta_folder / ncbi_id / ".fna", "fasta")
        elif ncbi_id in self.host_json:
            return SeqIO.parse(self.host_fasta_folder / ncbi_id / ".fna", "fasta")
        else:
            raise LookupError(f"Can't find {ncbi_id} in virus or host json file")

class DataExtractor(DataManager):
    
    TRAIN_JSON = "train.json"
    TEST_JSON = "test.json"

    def __init__(self, data_folder, tests_folder, feature_list):
        super().__init__(data_folder, tests_folder)
        self.feature_list = feature_list
        self.feature_data_map = self.load_feature_data(feature_list)

    def load_feature_data(self, feature_list):
        return {
            feature: pickle.load(open((self.features_folder / self.features_json[feature]["file"]), "rb"))
            for feature in feature_list
        }

    def run_data_extraction(self, cpu_count):
        data_filename = "---".join(self.feature_list).replace("/", "-") + ".pickle"
        process_pool = multiprocessing.Pool(cpu_count)

        train_extraciton_function = partial(
            self.extract_features_from_test_folder,
            filename=data_filename,
        )
        test_folders = list(self.tests_folder.glob("*"))
        chunksize = len(test_folders) // cpu_count

        logging.info(f"Start test_train_extraction using {cpu_count} CPUS and chunksize {chunksize}")
        for _ in process_pool.imap_unordered(
            func=train_extraciton_function, iterable=test_folders, chunksize=chunksize
        ):
            pass
        process_pool.close()
        logging.info(f"Done.")

    def extract_features_from_test_folder(self, test_folder, filename, check_existing_file = True):

        process_info = multiprocessing.current_process().name
        x_train = []
        y_train = []

        if check_existing_file and (test_folder / filename).exists():
            logging.info(
                f"Worker {process_info} skipping {test_folder / filename}, file exists!"
            )
            return True

        with open(test_folder / self.TRAIN_JSON) as fd:
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

        with open(test_folder / filename, "wb") as fd:
            pickle.dump([X, Y], fd)
            logging.info(f"Worker {process_info} saved file {filename} in {test_folder}")

        return True

    def get_features(self, virus, host):
        index = self.features_index[(virus, host)]
        return np.array([self.feature_data_map[feature][index] for feature in self.feature_list])

