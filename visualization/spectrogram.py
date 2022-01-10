import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

from utils import audioread, calculations
from single_signal import Signal
from letters.shape import Shape


class Spectrogram:
    signal: Signal
    max_time: float
    taxis: np.ndarray = None
    frqaxis: np.ndarray = None
    spectrogram: np.ndarray = None

    def __init__(self, sound, t):
        self.max_time = t
        self.signal = sound

    def calculate_spectrogram(self):
        window_size = np.ceil(10*self.signal.sampling_rate/1000)  # 10 ms window
        step_size = np.ceil(2*self.signal.sampling_rate/1000)  # 2 ms step
        n_per_segment = calculations.nextpow2(window_size)

        self.frqaxis, self.taxis, self.spectrogram = scipy.signal.spectrogram(x=self.signal.data,
                                                                              fs=self.signal.sampling_rate,
                                                                              nperseg=n_per_segment,
                                                                              noverlap=window_size-step_size,
                                                                              window='hamming')

    def normalize_spectrogram(self):
        self.spectrogram = self.spectrogram / np.min(self.spectrogram)

    def plot_spectrogram(self):
        # assert self.spectrogram is None, 'Spectrogram has not been calculated yet'
        plt.pcolormesh(self.taxis, self.frqaxis, self.spectrogram, shading='nearest')
        plt.title('Given audio signal in frequency and time domain')
        plt.xlabel('Time [s]')
        plt.ylabel('Frequencies [Hz]')
        plt.show()


if __name__ == '__main__':
    # Initial parameters
    path = '../test_audio/grilledcheesesandwich.wav'
    max_t = 4

    # Creating signal
    read_samples, read_sr = audioread.read_file(path, max_t)
    sig = Signal(read_samples, read_sr)

    # Creating shape
    letter_width = 0.5
    letter_length = 500
    letter_start = 0

    shp = Shape(letter_width, letter_length, letter_start, sig)
    shp.create_curve()
    sig.apply_shape(shp)

    audioread.plot_sound(sig.data, sig.sampling_rate)

    # Creating and plotting spectrogram after
    spec = Spectrogram(sig, max_t)
    spec.calculate_spectrogram()
    spec.normalize_spectrogram()
    spec.plot_spectrogram()
