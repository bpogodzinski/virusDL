#!/usr/bin/env python3

"""
    Luźne notatki

- blastn/eval10/best_hsp_bitscore_mean_normalization
- blastn/eval10/best_hsp_bitscore_mean_normalization_n50
- blastn/eval10/best_hsp_bitscore_min_max_normalization_n100
  - co to n50, n100?
  - różnica między mean a min-max
  - problem normalizacji (wartości znormalizowane i nieznormalizowane)
"""


from datetime import datetime
from pathlib import Path
from functools import partial
import logging
import multiprocessing
import os

from wirusy.DataExtractor import DataExtractor

# from wirusy.ModelFactory import ModelFactory

# Blastp eval - do rozkmininenia
FEATURE_LIST = [
    "blastn-rbo/eval10/rbo_unmerged_ranks_1000hits",
    "blastn/eval10/best_hsp_bitscore",
    "crispr/pilercr-default/max_mismatch2",
    "gc_content/difference",
    "kmer-canonical/k6/correlation_kendalltau",
]
CPU_COUNT_LOCAL = 1  # multiprocessing.cpu_count()

data_filename = "---".join(FEATURE_LIST).replace("/", "-") + ".pickle"
current_dir = Path(__file__).resolve().parent
(current_dir / "logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename=f'logs/learning_script-{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.log',
    format="%(levelname)s:%(asctime)s %(message)s",
    datefmt="[%d/%m/%Y %H:%M:%S]",
    level=logging.INFO,
)

logging.info(f"Setting up up DataExtractor")
extractor = DataExtractor(data_folder="data", tests_folder="tests", feature_list=FEATURE_LIST)
cpu_count = int(os.environ.get("SLURM_JOB_CPUS_PER_NODE", CPU_COUNT_LOCAL))
process_pool = multiprocessing.Pool(cpu_count)

train_extraciton_function = partial(
    extractor.extract_features_from_test_folder,
    save_to_file=True,
    filename=data_filename,
)
test_folders = list(extractor.tests_folder.glob("*"))
chunksize = len(test_folders) // cpu_count

logging.info(f"Start test_train_extraction using {cpu_count} CPUS and chunksize {chunksize}")
for _ in process_pool.imap_unordered(
    func=train_extraciton_function, iterable=test_folders, chunksize=chunksize
):
    pass
process_pool.close()
logging.info(f"Done.")
