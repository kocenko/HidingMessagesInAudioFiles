from typing import NoReturn
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

from utils import calculations
from visualization.single_signal import Signal


class Spectrogram:
    """A class which represents a spectrogram

    Attributes
    ----------
    signal : Signal
        a signal for which the spectrogram will be calculated
    taxis
        time axis returned from spectrogram calculations
    frqaxis
        frequency axis returned from spectrogram calculations
    spectrogram
        an array containing values returned from the spectrogram calculations

    Methods
    -------
    calculate_spectrogram
        calculating spectrogram parameters and spectrogram itself
    normalize_spectrogram
        normalizing values of the spectrogram so they are in the range of [0, 1]
    plot_spectrogram
        plotting spectrogram and labeling axes
    """

    def __init__(self, sound):
        """
        Parameters
        ----------
        sound:
            Signal class object representing created signal
        """

        self.signal: Signal = sound
        self.taxis = None
        self.frqaxis = None
        self.spectrogram = None

    def calculate_spectrogram(self) -> NoReturn:
        """Calculating spectrogram"""

        window_size = np.ceil(10*self.signal.sampling_rate/1000)  # 10 ms window
        step_size = np.ceil(3*self.signal.sampling_rate/1000)  # 3 ms step
        n_per_segment = calculations.nextpow2(window_size)

        self.frqaxis, self.taxis, self.spectrogram = scipy.signal.spectrogram(x=self.signal.data,
                                                                              fs=self.signal.sampling_rate,
                                                                              nperseg=n_per_segment,
                                                                              noverlap=window_size-step_size,
                                                                              window='hamming')

    def normalize_spectrogram(self):
        """Normalizing spectrogram"""

        divisor = np.max(self.spectrogram)
        if divisor:
            self.spectrogram = self.spectrogram / divisor
        else:
            print('Maximum value of the spectrogram is equal to 0. Cannot normalize')

    def plot_spectrogram(self) -> NoReturn:
        """Plotting created spectrogram"""

        assert self.spectrogram is not None, 'You need to create spectrogram first before plotting'

        plt.pcolormesh(self.taxis, self.frqaxis, self.spectrogram, shading='nearest')
        plt.title('Given audio signal in frequency and time domain')
        plt.xlabel('Time [s]')
        plt.ylabel('Frequencies [Hz]')
        plt.show()


if __name__ == '__main__':
    pass
