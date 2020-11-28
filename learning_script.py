#!/usr/bin/env python3

"""
    Luźne notatki

- blastn/eval10/best_hsp_bitscore_mean_normalization
- blastn/eval10/best_hsp_bitscore_mean_normalization_n50
- blastn/eval10/best_hsp_bitscore_min_max_normalization_n100
  - co to n50, n100?
  - różnica między mean a min-max
  - problem normalizacji (wartości znormalizowane i nieznormalizowane)

    

  Blastp eval - do rozkmininenia

"""


from datetime import datetime
from pathlib import Path
import logging
import os

from virusDL import FEATURE_LIST, CPU_COUNT_LOCAL
# from virusDL.DataManager import DataExtractor
from virusDL.DataManager import DataLoader
from virusDL.models.SimpleDeepLearningModel import SimpleDeepLearningModel
from virusDL.ModelManager import ModelManager


# extractor = DataExtractor(data_folder="data", tests_folder="tests", feature_list=FEATURE_LIST)
# cpu_count = int(os.environ.get("SLURM_JOB_CPUS_PER_NODE", CPU_COUNT_LOCAL))
# extractor.run_data_extraction(cpu_count)

loader = DataLoader(data_folder="data", tests_folder="tests", feature_list=FEATURE_LIST)
train_test_iterator = loader.get_train_test_data_iterator()

for test_folder, train_data, test_data in train_test_iterator:
    model_manager = ModelManager(SimpleDeepLearningModel, train_data, test_data, test_folder)
    model_manager.run()
    model_manager.evaluate()

"""wszystkie hosty z danym wirusem
wyciągam pary i przewiduje
roc
precision treccall curve


wirusy podobne do siebie
randomwoy split nie daje generalizacji 
"""
