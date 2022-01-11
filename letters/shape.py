from typing import NoReturn
from operator import add
import numpy as np
from scipy.signal import chirp


class Shape:

    _figure: np.ndarray = None

    def __init__(self, sound, start_t, start_f, width, x_dir: bool = True):
        self.width = width  # In sec
        self.start_point_t = start_t  # In sec
        self.start_point_f = start_f  # In Hz
        self.template = sound
        self.figure: np.ndarray = np.zeros(int(width * sound.sampling_rate))
        self.x_direction: bool = x_dir

        assert np.ceil(self.template.sampling_rate * (self.start_point_t + self.width)) <= len(self.template.data), \
            'Cannot create a symbol of given width at given starting point'

    @property
    def figure(self):
        return self._figure

    @figure.setter
    def figure(self, new_fig: np.ndarray):
        if new_fig.ndim > 1:
            raise ValueError(f'Figure implementation cannot have more than one dimension')
        else:
            self._figure = new_fig

    def create_shape(self) -> NoReturn:
        raise NotImplementedError

    def _combine_figures(self, fig: np.ndarray, x_dir: bool):
        if fig.size > self.figure.size:
            raise ValueError(f'Combined figure size cannot be bigger than the size of the base figure')
        else:
            dif_in_len = self.figure.size - fig.size
            zeros_array = np.zeros(dif_in_len)

            if x_dir:
                fig = np.append(fig, zeros_array)
            else:
                fig = np.append(zeros_array, fig)

            print(fig)
            self.figure = np.array(list(map(add, self.figure, fig)))

    def _scale_figure(self) -> NoReturn:
        scale = 1
        divisor = np.mean(np.abs(self.figure))
        if divisor:
            scale = np.mean(np.abs(self.template.data)) / divisor
        self.figure = self.figure * scale

    def _calculate_t_axis(self):
        fs = self.template.sampling_rate
        t = np.arange(0, self.width * fs - 1, 1) / fs
        return t


class Curve(Shape):

    def __init__(self, sound, start_t, start_f, width, height, x_dir: bool = True, desc: bool = False):
        super().__init__(sound, start_t, start_f, width, x_dir)

        self.height = height
        self.descending = desc

        assert np.ceil(self.start_point_f + self.height) <= self.template.sampling_rate / 2, \
            'Cannot create a symbol of given height at given starting point'
        assert self.height > 0, 'Height of the shape has to be positive'

    def create_shape(self) -> NoReturn:
        t = self._calculate_t_axis()

        print(f'Creating curve at parameters\n'
              f'start_t: {self.start_point_t} [s]\n'
              f'start_f: {self.start_point_f} [Hz]\n'
              f'width: {self.width} [s]\n'
              f'height: {self.height} [Hz]\n'
              f'x_dir: {self.x_direction}\n'
              f'from right: {self.x_direction}\n')

        f0 = self.start_point_f
        f1 = self.start_point_f + self.height

        if self.descending:
            f0 = f1
            f1 = self.start_point_f

        t1 = self.width

        print(f'Chirp parameters:\n'
              f'Starting frq: {f0}\n'
              f'Ending frq: {f1}\n'
              f'Duration: {t1}\n')

        # Creating chirp signal
        self.figure = chirp(t, f0, t1, f1, method='linear')
        self._scale_figure()


class VerticalLine(Shape):

    def __init__(self, sound, start_t, start_f, width, height, x_dir: bool = True, y_dir: bool = True):
        super().__init__(sound, start_t, start_f, width, x_dir)
        self.height = height
        self.y_direction = y_dir

        assert np.ceil(self.start_point_f + self.height) <= self.template.sampling_rate / 2, \
            'Cannot create a symbol of given height at given starting point'
        assert self.height > 0, 'Height of the shape has to be positive'

    def create_shape(self) -> NoReturn:
        t = self._calculate_t_axis()

        # Calculating ending points
        f0 = self.start_point_f
        f1 = self.start_point_f + self.height

        print(f'Creating vertical line at parameters\n'
              f'start_t: {self.start_point_t} [s]\n'
              f'start_f: {self.start_point_f} [Hz]\n'
              f'width: {self.width} [s]\n'
              f'height: {self.height} [Hz]\n'
              f'x_dir: {self.x_direction}\n'
              f'y_dir: {self.y_direction}\n')

        # Creating noise signal
        spread = 50  # Experimental value
        noise_signal = 0
        frequency_range = np.arange(f0, f1, self.height/spread)
        for f in frequency_range:
            noise_signal = noise_signal + np.sin(2 * np.pi * f * t)

        self.figure = noise_signal
        self._scale_figure()


class HorizontalLine(Shape):

    def __init__(self, sound, start_t, start_f, width, x_dir: bool = True):
        super().__init__(sound, start_t, start_f, width, x_dir)

    def create_shape(self) -> NoReturn:
        t = self._calculate_t_axis()
        f0 = self.start_point_f

        print(f'Creating horizontal line at parameters\n'
              f'start_t: {self.start_point_t} [s]\n'
              f'start_f: {self.start_point_f} [Hz]\n'
              f'width: {self.width} [s]\n'
              f'x_dir: {self.x_direction}\n')

        self.figure = np.sin(2 * np.pi * f0 * t)
        self._scale_figure()
