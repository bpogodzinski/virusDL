from .BaseModel import BaseModel
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

class SimpleDeepLearningModel(BaseModel):
    NAME = 'DeepNN'
    def __init__(self):
        super().__init__()
        self.model = self.__create_model()

    def __create_model(self):
        model = Sequential()
        model.add(Dense(128, activation="relu"))
        model.add(Dense(128, activation="relu"))
        model.add(Dense(1, activation="sigmoid"))
        model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
        return model