import numpy as np


class Signal:

    def __init__(self, samples, sr):
        self._data: np.ndarray = samples
        self._sampling_rate: float = sr

    @property
    def data(self):
        return self.data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def sampling_rate(self):
        return self.sampling_rate

    @sampling_rate.setter
    def sampling_rate(self, sr):
        self._sampling_rate = sr
