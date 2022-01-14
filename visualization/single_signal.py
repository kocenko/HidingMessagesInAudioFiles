from typing import NoReturn
from operator import add
import numpy as np
import soundfile as sf

from letters.shape import Shape


class Signal:
    """A class which represents loaded signal

    Attributes
    ----------
    _data : np.ndarray
        samples containing values of amplitudes at certain time points
    _sampling_rate : float
        self-explanatory

    Methods
    -------
    save_signal(path: str)
        Saving singnal at given path
    apply_shape(shape: Shape)
        Applying shape features to the signal
    """

    def __init__(self, samples, sr):
        """
        Parameters
        ----------
        samples
            samples returned from function reading data from audio file
        sr
            sampling rate
        """

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

    def save_signal(self, path: str) -> NoReturn:
        """Function saving created signal to given path

        Parameters
        ----------
        path : str
            path to save created signal to
        """

        sf.write(path, self.data, int(self.sampling_rate), subtype='PCM_24')

    def apply_shape(self, shape: Shape) -> NoReturn:
        """Applying shape to the signal

        Parameters
        ----------
        shape : Shape
            shape to be applied to the signal
        """

        beg_idx = int(np.ceil(shape.start_point_t * self._sampling_rate))
        end_idx = int(np.ceil((shape.start_point_t + shape.width) * self._sampling_rate)) - 1

        # Slicing whole signal into three parts and applying signal to the second part
        self.data = np.array(list(self.data[:beg_idx])
                             + list(map(add, self.data[beg_idx:end_idx], shape.figure))
                             + list(self.data[end_idx:]))
