import json
from pathlib import Path
from virusDL import TENSORBOARD_LOG_DIR

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import TensorBoard


class ModelManager:
    def __init__(self, cls, X, Y, features_string):
        self.model_class = cls()
        self.model = self.model_class.get_model()
        self.model_name = self.model_class.get_name()
        self.X = X
        self.Y = Y
        self.final_model_name = f"{self.model_name}--{features_string}"
        self.tensorboard = TensorBoard(log_dir=TENSORBOARD_LOG_DIR / self.final_model_name)

    def run(self):
        self.model.fit(self.X, self.Y, epochs = 100, batch_size = 16, shuffle = True, callbacks = [self.tensorboard])

    def test(self, test_folder):
        TRAIN_JSON = 'train.json'
        viruses = json.load(open(test_folder / TRAIN_JSON))['vids']
        










