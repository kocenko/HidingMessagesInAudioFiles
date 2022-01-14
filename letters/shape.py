from typing import NoReturn
from operator import add
import numpy as np
from scipy.signal import chirp


class Shape:
    """A class which represents a single shape

    Attributes
    ----------
    id_name : str
        a string representing single shape name
    template
        a base sound as a Signal class object, used as a template for calculations
    start_point_t
        a floating point number representing the beginning of the figure - left border [in seconds]
    start_point_f
        a floating point number representing the beginning of the figure - bottom border [in HZ]
    width
        a floating point number representing the width of the figure [in seconds]
    height
        a floating point number representing the height of the figure [in Hz]
    _figure : np.ndarray
        numpy array representing signal alteration which creates shapes in time and frequency domain

    Methods
    -------
    _combine_figures(fig: np.ndarray, start_t)
        Merges the base figure with the new one
    _scale_figure()
        Scales the amplitude of the alteration of the signal to make it dimmer at the spectrogram
    _calculate_t_axis()
        Calculates an array of time change based on the sampling rate
    """

    def __init__(self, sound, start_t, start_f, width, height):
        """
        Parameters
        ----------
        sound
            a base sound as a Signal class object, used as a template for calculations
        start_t
            a floating point number representing the beginning of the figure - left border [in seconds]
        start_f
            a floating point number representing the beginning of the figure - bottom border [in HZ]
        width
            a floating point number representing the width of the figure [in seconds]
        height
            a floating point number representing the height of the figure [in Hz]

        Raises
        -----
        AssertionError
            If the parameters of the position and the size cause figure not to fit in range
        """

        self.id_name: str = ''
        self.width = width  # In sec
        self.height = height  # In Hz
        self.start_point_t = start_t  # In sec
        self.start_point_f = start_f  # In Hz
        self.template = sound
        self._figure: np.ndarray = np.zeros(int(width * sound.sampling_rate))

        assert np.ceil(self.template.sampling_rate * (self.start_point_t + self.width)) <= len(self.template.data), \
            'Cannot create a symbol of given width at given starting point'
        assert self.width >= 0, 'Width of the shape has to be positive'

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

    def _combine_figures(self, fig: np.ndarray, start_t) -> NoReturn:
        """Combining base figure with the given one at the given starting point

        Parameters
        ----------
        fig : np.ndarray
            an array of the figure that is to be merged with the base figure
        start_t
            starting time at which the given figure is to be merged with the base figure

        Raises
        ------
        ValueError
            When the size of the given figure is bigger than the base figure
        ValueError
            When the beginning of the given figure is before the beginning of the base figure
        """

        if fig.size > self.figure.size:
            raise ValueError(f'Combined figure size cannot be bigger than the size of the base figure')
        else:
            precision = 1.e-9

            # Calculating the beginning index
            if start_t < self.start_point_t:
                raise ValueError('Beginning time of the shape cannot be less than starting point of the base')
            beg_len = int(np.floor((start_t - self.start_point_t) * self.template.sampling_rate))

            # Calculating the ending index
            if self.figure.size - (beg_len + fig.size) < precision:
                end_len = int(abs(np.floor(self.figure.size - (beg_len + fig.size))))
            else:
                end_len = int(np.floor(self.figure.size - (beg_len + fig.size)))

            # Creating complement arrays
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
                # print('Figure combination: Complement is not required')
                pass

            self.figure = np.array(list(map(add, self.figure, fig)))

    def _scale_figure(self) -> NoReturn:
        """Scaling figure

        Scales the amplitude of the alteration of the signal to make it dimmer at the spectrogram
        """

        scale = 1  # Not scaling at all
        divisor = np.mean(np.abs(self.figure))
        if divisor:
            scale = np.max(np.abs(self.template.data)) / divisor
        self.figure = self.figure * scale

    def _calculate_t_axis(self):
        """Calculating time array

        Calculates an array of time change based on the sampling rate
        """

        fs = self.template.sampling_rate
        t = np.arange(0, self.width * fs, 1) / fs
        return t


class Curve(Shape):
    """A class which is representing diagonal line and curves

    A curve name comes from the idea where it originally represented only curved shapes of the letter.
    When the radius of curvature is infinite than it becomes a line (here a diagonal line).

    Attributes
    ----------
    descending : bool
        a bool representing a logical value of the fact of the descent of the line
    round : bool
        a bool representing a logical value of the fact of the roundness of the line

    Methods
    -------
    create_shape()
        changes figure from the zero array to the array with created signal
    """

    def __init__(self, sound, start_t, start_f, width, height, desc: bool = False, rnd: str = 'l'):
        """
        Parameters
        ----------
        sound
            a base sound as a Signal class object, used as a template for calculations
        start_t
            a floating point number representing the beginning of the figure - left border [in seconds]
        start_f
            a floating point number representing the beginning of the figure - bottom border [in HZ]
        width
            a floating point number representing the width of the figure [in seconds]
        height
            a floating point number representing the height of the figure [in Hz]
        desc : bool
            a bool representing a logical value of the fact of the descent of the line
        rnd : str
            a str representing a type of roundness
        """

        super().__init__(sound, start_t, start_f, width, height)
        self.descending = desc
        self.round = rnd
        self.id_name = 'Curve'

    def create_shape(self) -> NoReturn:
        """Creates shape

        Changes figure from the zero array to the array with created signal - chirp signal.
        """

        t = self._calculate_t_axis()

        f0 = self.start_point_f
        f1 = self.start_point_f + self.height
        t1 = self.width

        if self.descending:
            f0 = f1
            f1 = self.start_point_f

        # Choosing type of curve
        if self.round == 't' and self.descending:
            method = 'quadratic'
        elif self.round == 't' and not self.descending:
            method = 'logarithmic'
        elif self.round == 'b':
            method = 'hyperbolic'
        else:
            method = 'linear'

        # Creating chirp signal
        self.figure = chirp(t, f0, t1, f1, method=method)
        self._scale_figure()


class VerticalLine(Shape):
    """A class which is vertical line

    Methods
    -------
    create_shape()
        changes figure from the zero array to the array with created signal
    """

    def __init__(self, sound, start_t, start_f, width, height):
        """
        Parameters
        ----------
        sound
            a base sound as a Signal class object, used as a template for calculations
        start_t
            a floating point number representing the beginning of the figure - left border [in seconds]
        start_f
            a floating point number representing the beginning of the figure - bottom border [in HZ]
        width
            a floating point number representing the width of the figure [in seconds]
        height
            a floating point number representing the height of the figure [in Hz]
        """

        super().__init__(sound, start_t, start_f, width, height)
        self.id_name = 'Vline'

    def create_shape(self) -> NoReturn:
        """Creates shape

        Changes figure from the zero array to the array with created signal - sine waves with range of frequencies.
        """

        t = self._calculate_t_axis()

        # Calculating ending points
        f0 = self.start_point_f
        f1 = self.start_point_f + self.height

        # Creating noise signal
        spread = 50  # Experimental value
        noise_signal = np.zeros(t.size)
        frequency_range = np.arange(f0, f1, self.height/spread)
        for f in frequency_range:
            noise_signal = np.array(list(map(add, noise_signal, np.sin(2 * np.pi * f * t))))

        self.figure = noise_signal
        self._scale_figure()


class HorizontalLine(Shape):
    """A class which is vertical line

    Methods
    -------
    create_shape()
        changes figure from the zero array to the array with created signal
    """

    def __init__(self, sound, start_t, start_f, width, height):
        """
        Parameters
        ----------
        sound
            a base sound as a Signal class object, used as a template for calculations
        start_t
            a floating point number representing the beginning of the figure - left border [in seconds]
        start_f
            a floating point number representing the beginning of the figure - bottom border [in HZ]
        width
            a floating point number representing the width of the figure [in seconds]
        height
            a floating point number representing the height of the figure [in Hz]
        """

        super().__init__(sound, start_t, start_f, width, height)
        self.id_name = 'Hline'

    def create_shape(self) -> NoReturn:
        """Creates shape

         Changes figure from the zero array to the array with created signal - single sine wave.
        """

        t = self._calculate_t_axis()
        f0 = self.start_point_f

        self.figure = np.sin(2 * np.pi * f0 * t)
        self._scale_figure()
