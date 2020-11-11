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
import logging
import os

from wirusy.DataManager import DataExtractor

CPU_COUNT_LOCAL = 1  # multiprocessing.cpu_count()

# Blastp eval - do rozkmininenia
FEATURE_LIST = [
    "blastn-rbo/eval10/rbo_unmerged_ranks_1000hits",
    "blastn/eval10/best_hsp_bitscore",
    "crispr/pilercr-default/max_mismatch2",
    "gc_content/difference",
    "kmer-canonical/k6/correlation_kendalltau",
]

current_dir = Path(__file__).resolve().parent
(current_dir / "logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename=f'logs/learning_script-{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.log',
    format="%(levelname)s:%(asctime)s %(message)s",
    datefmt="[%d/%m/%Y %H:%M:%S]",
    level=logging.INFO,
)



extractor = DataExtractor(data_folder="data", tests_folder="tests", feature_list=FEATURE_LIST)
cpu_count = int(os.environ.get("SLURM_JOB_CPUS_PER_NODE", CPU_COUNT_LOCAL))
extractor.run_data_extraction(cpu_count)