from datetime import datetime
from pathlib import Path
import logging

CPU_COUNT_LOCAL = 1  # multiprocessing.cpu_count()
CURRENT_DIR = Path(__file__).resolve().parent
LOG_DIR = CURRENT_DIR / 'logs'
TENSORBOARD_LOG_DIR = CURRENT_DIR / 'tensorboard_logs'
LOG_DIR.mkdir(exist_ok=True)
TENSORBOARD_LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    filename=f'{LOG_DIR}/learning_script-{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.log',
    format="%(levelname)s:%(asctime)s %(message)s",
    datefmt="[%d/%m/%Y %H:%M:%S]",
    level=logging.INFO,
)