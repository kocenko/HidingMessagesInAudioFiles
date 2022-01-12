import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

from utils import audioread, calculations
from single_signal import Signal
from letters.letter import Letter


class Spectrogram:
    signal: Signal
    max_time: float
    taxis: np.ndarray = None
    frqaxis: np.ndarray = None
    spectrogram: np.ndarray = None

    def __init__(self, sound):
        self.signal = sound

    def calculate_spectrogram(self):
        window_size = np.ceil(10*self.signal.sampling_rate/1000)  # 10 ms window
        step_size = np.ceil(3*self.signal.sampling_rate/1000)  # 3 ms step
        n_per_segment = calculations.nextpow2(window_size)

        self.frqaxis, self.taxis, self.spectrogram = scipy.signal.spectrogram(x=self.signal.data,
                                                                              fs=self.signal.sampling_rate,
                                                                              nperseg=n_per_segment,
                                                                              noverlap=window_size-step_size,
                                                                              window='hamming')

    def normalize_spectrogram(self):
        divisor = np.max(self.spectrogram)
        if divisor:
            self.spectrogram = self.spectrogram / divisor
        else:
            print('Maximum value of the spectrogram is equal to 0. Cannot normalize')

    def plot_spectrogram(self):
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
    letter_width = 0.2
    letter_height = 3000
    letter_start_t = 1
    letter_start_f = 4000

    # Curve(sig, letter_start_t, letter_start_f, letter_width, letter_height)
    letter = Letter(sig, letter_start_t, letter_start_f, letter_width, letter_height, 'A')
    letter.create_shape()
    sig.apply_shape(letter)

    audioread.plot_sound(sig.data, sig.sampling_rate)

    # Creating and plotting spectrogram after
    spec = Spectrogram(sig)
    spec.calculate_spectrogram()
    spec.normalize_spectrogram()
    spec.plot_spectrogram()
