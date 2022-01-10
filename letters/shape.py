from typing import NoReturn
import numpy as np
from scipy.signal import chirp


class Shape:

    figure = None

    def __init__(self, sound, start_t, start_f, width):
        self.width = width  # In sec
        self.start_point_t = start_t  # In sec
        self.start_point_f = start_f  # In Hz
        self.template = sound

        assert np.ceil(self.template.sampling_rate * (self.start_point_t + self.width)) <= len(self.template.data), \
            'Cannot create a symbol of given width at given starting point'

    def create_shape(self) -> NoReturn:
        raise NotImplementedError

    def _scale_figure(self) -> NoReturn:
        scale = np.mean(np.abs(self.template.data)) / np.mean(np.abs(self.figure))
        self.figure = self.figure * scale

    def _calculate_t_axis(self):
        fs = self.template.sampling_rate
        t = np.arange(self.start_point_t, (self.start_point_t + self.width) * fs - 1, 1) / fs
        return t


class Curve(Shape):

    def __init__(self, sound, start_t, start_f, width, height):
        super().__init__(sound, start_t, start_f, width)
        self.height = height

        assert np.ceil(self.start_point_f + self.height) <= self.template.sampling_rate / 2, \
            'Cannot create a symbol of given height at given starting point'

    def create_shape(self) -> NoReturn:
        t = self._calculate_t_axis()

        # Calculating ending points
        f0 = self.start_point_f
        f1 = self.start_point_f + self.height
        t1 = self.width

        # Creating chirp signal
        self.figure = chirp(t=t, f0=f0, f1=f1, t1=t1, method='linear')
        self._scale_figure()


class VerticalLine(Shape):

    def __init__(self, sound, start_t, start_f, width, height):
        super().__init__(sound, start_t, start_f, width)
        self.height = height

        assert np.ceil(self.start_point_f + self.height) <= self.template.sampling_rate / 2, \
            'Cannot create a symbol of given height at given starting point'

    def create_shape(self) -> NoReturn:
        t = self._calculate_t_axis()

        # Calculating ending points
        f0 = self.start_point_f
        f1 = self.start_point_f + self.height

        # Creating noise signal
        spread = 50  # Experimental value
        noise_signal = 0
        frequency_range = np.arange(f0, f1, self.height/spread)
        for f in frequency_range:
            noise_signal = noise_signal + np.sin(2 * np.pi * f * t)

        self.figure = noise_signal
        self._scale_figure()
