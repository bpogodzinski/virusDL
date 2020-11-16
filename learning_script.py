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

from virusDL import CPU_COUNT_LOCAL
from virusDL.DataManager import DataExtractor
# from virusDL.models.SimpleDeepLearningModel import SimpleDeepLearningModel
# from virusDL.ModelManager import ModelManager

FEATURE_LIST = [
    "blastn-rbo/eval10/rbo_unmerged_ranks_1000hits",
    "blastn/eval10/best_hsp_bitscore",
    "crispr/pilercr-default/max_mismatch2",
    "gc_content/difference",
    "kmer-canonical/k6/correlation_kendalltau",
]


extractor = DataExtractor(data_folder="data", tests_folder="tests", feature_list=FEATURE_LIST)
cpu_count = int(os.environ.get("SLURM_JOB_CPUS_PER_NODE", CPU_COUNT_LOCAL))
extractor.run_data_extraction(cpu_count)

# wyciągam dane do uczenia
# loader = DataLoader(data_folder="data", tests_folder="tests", feature_list=FEATURE_LIST)
# training_iterator = loader.get_training_data_iterator()

# for test_folder, X, Y in training_iterator:
#     name = f'{test_folder.parts[-1]}---{loader.get_filename(no_extension=True)}'
#     model_manager = ModelManager(SimpleDeepLearningModel, X, Y, name)
#     model_manager.run()


"""wszystkie hosty z danym wirusem
wyciągam pary i przewiduje
roc
precision treccall curve


wirusy podobne do siebie
randomwoy split nie daje generalizacji 
"""
