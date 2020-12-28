from datetime import datetime
from pathlib import Path
import logging

CPU_COUNT_LOCAL = 1  # multiprocessing.cpu_count()
CURRENT_DIR = Path(__file__).resolve().parent
RESULT_DIR = CURRENT_DIR / 'results'
LOG_DIR = CURRENT_DIR / 'logs'
TENSORBOARD_LOG_DIR = CURRENT_DIR / 'tensorboard_logs'
LOG_DIR.mkdir(exist_ok=True)
TENSORBOARD_LOG_DIR.mkdir(exist_ok=True)
FEATURE_LIST = [
    "blastn-rbo/eval10/rbo_unmerged_ranks_1000hits",
    "blastn/eval10/best_hsp_bitscore",
    "crispr/pilercr-default/max_mismatch2",
    "gc_content/difference",
    "kmer-canonical/k6/correlation_kendalltau",
]
logging.basicConfig(
    filename=f'{LOG_DIR}/learning_script-{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.log',
    format="%(levelname)s:%(asctime)s %(message)s",
    datefmt="[%d/%m/%Y %H:%M:%S]",
    level=logging.INFO,
)