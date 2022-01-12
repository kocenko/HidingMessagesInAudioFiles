from typing import NoReturn
from operator import add
import numpy as np
from scipy.signal import chirp


class Shape:

    _figure: np.ndarray = None
    id_name: str = None

    def __init__(self, sound, start_t, start_f, width, height):
        self.width = width  # In sec
        self.height = height  # In Hz
        self.start_point_t = start_t  # In sec
        self.start_point_f = start_f  # In Hz
        self.template = sound
        self.figure: np.ndarray = np.zeros(int(width * sound.sampling_rate))

        assert np.ceil(self.template.sampling_rate * (self.start_point_t + self.width)) <= len(self.template.data), \
            'Cannot create a symbol of given width at given starting point'

        assert np.ceil(self.start_point_f + self.height) <= self.template.sampling_rate / 2, \
            'Cannot create a symbol of given height at given starting point'
        assert self.height >= 0, 'Height of the shape has to be positive'

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

    def _combine_figures(self, fig: np.ndarray, start_t):
        if fig.size > self.figure.size:
            raise ValueError(f'Combined figure size cannot be bigger than the size of the base figure')
        else:
            precision = 1.e-9
            if start_t < self.start_point_t:
                raise ValueError('Beginning time of the shape cannot be less than starting point of the base')
            beg_len = int(np.floor((start_t - self.start_point_t) * self.template.sampling_rate))

            if self.figure.size - (beg_len + fig.size) < precision:
                end_len = int(abs(np.floor(self.figure.size - (beg_len + fig.size))))
            else:
                end_len = int(np.floor(self.figure.size - (beg_len + fig.size)))

            beg_array = np.zeros(beg_len)
            end_array = np.zeros(end_len)

            if not beg_len and end_len:
                # There is no beginning complement required
                fig = np.append(fig, end_array)

            elif beg_len and not end_len:
                # There is no end complement required
                fig = np.append(beg_array, fig)

            elif beg_len and end_len:
                # There is a beginning and an end complement required
                fig = np.append(beg_array, fig)
                fig = np.append(fig, end_array)

            else:
                print('Figure combination: Complement is not required')

            self.figure = np.array(list(map(add, self.figure, fig)))

    def _scale_figure(self) -> NoReturn:
        scale = 1
        divisor = np.mean(np.abs(self.figure))
        if divisor:
            scale = np.mean(np.abs(self.template.data)) / divisor
        self.figure = self.figure * scale

    def _calculate_t_axis(self):
        fs = self.template.sampling_rate
        t = np.arange(0, self.width * fs, 1) / fs
        return t


class Curve(Shape):

    def __init__(self, sound, start_t, start_f, width, height, desc: bool = False):
        super().__init__(sound, start_t, start_f, width, height)
        self.descending = desc
        self.id_name = 'Curve'

    def create_shape(self) -> NoReturn:
        t = self._calculate_t_axis()

        # print(f'Creating curve at parameters\n'
        #       f'start_t: {self.start_point_t} [s]\n'
        #       f'start_f: {self.start_point_f} [Hz]\n'
        #       f'width: {self.width} [s]\n'
        #       f'height: {self.height} [Hz]\n')

        f0 = self.start_point_f
        f1 = self.start_point_f + self.height

        if self.descending:
            f0 = f1
            f1 = self.start_point_f

        t1 = self.width

        # Creating chirp signal
        self.figure = chirp(t, f0, t1, f1, method='linear')
        self._scale_figure()


class VerticalLine(Shape):

    def __init__(self, sound, start_t, start_f, width, height):
        super().__init__(sound, start_t, start_f, width, height)
        self.id_name = 'Vline'

    def create_shape(self) -> NoReturn:
        t = self._calculate_t_axis()

        # Calculating ending points
        f0 = self.start_point_f
        f1 = self.start_point_f + self.height

        # print(f'Creating vertical line at parameters\n'
        #       f'start_t: {self.start_point_t} [s]\n'
        #       f'start_f: {self.start_point_f} [Hz]\n'
        #       f'width: {self.width} [s]\n'
        #       f'height: {self.height} [Hz]\n')

        # Creating noise signal
        spread = 50  # Experimental value
        noise_signal = np.zeros(t.size)
        frequency_range = np.arange(f0, f1, self.height/spread)
        for f in frequency_range:
            noise_signal = np.array(list(map(add, noise_signal, np.sin(2 * np.pi * f * t))))

        self.figure = noise_signal
        self._scale_figure()


class HorizontalLine(Shape):

    def __init__(self, sound, start_t, start_f, width, height):
        super().__init__(sound, start_t, start_f, width, height)
        self.id_name = 'Hline'

    def create_shape(self) -> NoReturn:
        t = self._calculate_t_axis()
        f0 = self.start_point_f

        # print(f'Creating horizontal line at parameters\n'
        #       f'start_t: {self.start_point_t} [s]\n'
        #       f'start_f: {self.start_point_f} [Hz]\n'
        #       f'width: {self.width} [s]\n')

        self.figure = np.sin(2 * np.pi * f0 * t)
        self._scale_figure()
