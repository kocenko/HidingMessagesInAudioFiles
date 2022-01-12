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
        beg_idx = int(np.ceil(shape.start_point_t * self._sampling_rate))
        end_idx = int(np.ceil((shape.start_point_t + shape.width) * self._sampling_rate)) - 1

        # plt.plot(shape.figure)
        # plt.title('Signal shape outcome')
        # plt.show()

        self.data = np.array(list(self.data[:beg_idx])
                             + list(map(add, self.data[beg_idx:end_idx], shape.figure))
                             + list(self.data[end_idx:]))
