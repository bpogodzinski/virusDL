from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


class ModelFactory:

    def get_model(self):
        model = Sequential()
        model.add(Dense(128, activation='relu'))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.add(Dense(2, activation='softmax'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

ModelFactory().get_model()