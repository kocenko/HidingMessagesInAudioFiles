from operator import add
import numpy as np

from letters.shape import Shape


class Signal:

    def __init__(self, samples, sr):
        self._data: np.ndarray = samples
        self._sampling_rate: float = sr

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def sampling_rate(self):
        return self._sampling_rate

    @sampling_rate.setter
    def sampling_rate(self, sr):
        self._sampling_rate = sr

    def apply_shape(self, shape: Shape):
        if len(self.data) < (shape.start_point + shape.width):
            raise ValueError('Cannot fit the shape into the signal')
        else:
            beg_idx = int(np.ceil(shape.start_point * self._sampling_rate))
            end_idx = int(np.ceil((shape.start_point + shape.width) * self._sampling_rate)) - 1

            print(f'Slice size ({beg_idx}, {end_idx}): {end_idx-beg_idx+1}, Curve size: {len(shape.curve)}')

            output1 = list(self.data[:beg_idx])
            output2 = list(map(add, self.data[beg_idx:end_idx], shape.curve))
            output3 = list(self.data[end_idx:])

            self.data = np.array(output1 + output2 + output3)
