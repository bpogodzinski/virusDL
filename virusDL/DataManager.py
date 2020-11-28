import logging
import multiprocessing
import os
import pickle
import json
from pathlib import Path
from functools import partial

import numpy as np
import pandas as pd

from Bio import SeqIO


def features_to_filename(feature_list):
    return "---".join(feature_list).replace("/", "-") + ".pickle"


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
        self.positive_pairs = pd.read_csv(os.path.join(data_folder, "positive_pairs.csv"))

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
        data_filename = features_to_filename(self.feature_list)
        process_pool = multiprocessing.Pool(cpu_count)

        train_extraciton_function = partial(
            self.extract_train_test_from_test_folder,
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

    def extract_train_test_from_test_folder(self, test_folder, filename, check_existing_file=False):

        process_info = multiprocessing.current_process().name
        filename_test = filename + ".test"
        x_train = []
        y_train = []
        x_test = []
        y_test = []
        ids_test = []

        if check_existing_file and (test_folder / filename).exists():
            logging.info(f"Worker {process_info} skipping {test_folder / filename}, file exists!")
        else:
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

            X_train, Y_train = np.array(x_train), np.array(y_train)

            with open(test_folder / filename, "wb") as fd:
                pickle.dump([X_train, Y_train], fd)
                logging.info(f"Worker {process_info} saved file {filename} in {test_folder}")

        if check_existing_file and (test_folder / filename_test).exists():
            logging.info(f"Worker {process_info} skipping {test_folder / filename_test}, file exists!")
        else:
            with open(test_folder / self.TEST_JSON) as fd:
                train_viruses = json.load(fd)["vids"]
                all_hosts = list(self.host_fasta_folder.glob("*"))
                len_all = len(train_viruses) * len(all_hosts)
                counter_all = 1
                for virus_id in train_viruses:
                    for host in all_hosts:
                        host_id = host.parts[-1].split(".")[0]
                        logging.info(
                            f"Worker {process_info} doing test {[virus_id, host_id]} from {test_folder} {counter_all}/{len_all}"
                        )
                        x = self.get_features(virus_id, host_id)
                        y = int((self.positive_pairs[["virus", "host"]].values == [virus_id, host_id]).all(axis=1).any())
                        x_test.append(x)
                        y_test.append(y)
                        ids_test.append([virus_id, host_id])
                        counter_all += 1
                        
            X_test, Y_test, ID_test = np.array(x_test), np.array(y_test), np.array(ids_test)
            with open(test_folder / filename_test, "wb") as fd:
                pickle.dump([X_test, Y_test, ID_test], fd)
                logging.info(f"Worker {process_info} saved file {filename_test} in {test_folder}")
        
        return True

    def get_features(self, virus, host):
        index = self.features_index[(virus, host)]
        return np.array([self.feature_data_map[feature][index] for feature in self.feature_list])


class DataLoader(DataManager):
    def __init__(self, data_folder, tests_folder, feature_list):
        super().__init__(data_folder, tests_folder)
        self.feature_list = feature_list

    def get_filename(self, no_extension=False):
        filename = features_to_filename(self.feature_list)
        if no_extension:
            return filename.split(".")[0]
        return filename

    def get_train_test_data_iterator(self):
        for test_folder in self.tests_folder.glob("*"):
            train = pickle.load(open(test_folder / self.get_filename(), "rb"))
            test = pickle.load(open(test_folder / (self.get_filename() + '.test'), "rb"))
            yield test_folder, train, test