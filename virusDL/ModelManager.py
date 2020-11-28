import json
from json import load
from pathlib import Path
from itertools import groupby
from typing import DefaultDict
from virusDL import TENSORBOARD_LOG_DIR, FEATURE_LIST
from virusDL.DataManager import features_to_filename

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import TensorBoard


class ModelManager:
    def __init__(self, cls, train, test, test_folder):
        self.model_class = cls()
        self.model = self.model_class.get_model()
        self.model_name = self.model_class.get_name()
        self.train_data = train
        self.test_data = test
        self.folder = test_folder
        self.features_name = f'{test_folder.parts[-1]}---{features_to_filename(FEATURE_LIST).split(".")[0]}'
        self.final_model_name = f"{self.model_name}--{self.features_name}"
        self.tensorboard = TensorBoard(log_dir=TENSORBOARD_LOG_DIR / self.final_model_name)

    def run(self):
        if (self.folder / self.final_model_name).exists():
            self.model = load_model(self.folder / self.final_model_name)
        else:
            X = np.array([x for x in self.train_data[0]])
            Y = np.array([y for y in self.train_data[1]])
            self.model.fit(X, Y, epochs = 100, batch_size = 16, shuffle = True, callbacks = [self.tensorboard])
            self.model.save(self.folder / self.final_model_name)


    # pogrupuj 
    def evaluate(self):
        result_dict = DefaultDict(list)
        test_dict = DefaultDict(list)
        x_test = np.array([x for x in self.test_data[0]])
        pairs = np.array([pair for pair in self.test_data[2]])
        for pair, X in zip(pairs, x_test):
            virus_id = pair[0]
            test_dict[virus_id].append([pair[1], X])

        for virus_id in test_dict.keys():
            hosts_id = [x[0] for x in test_dict[virus_id]]
            x_array = np.array([x[1] for x in test_dict[virus_id]])
            predictions = self.model.predict(x_array).reshape(-1).tolist()
            result_dict[virus_id] = sorted([[host, pred] for host, pred in zip(hosts_id, predictions)], key=lambda x: x[1], reverse=True)

        
        json.dump(result_dict, open(self.folder / 'results.json','w'))









