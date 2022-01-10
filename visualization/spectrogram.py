import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt

from utils import audioread, calculations
from visualization.single_signal import Signal


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
        window_size = np.ceil(100*self.signal.sampling_rate/1000)  # 100 ms window
        step_size = np.ceil(20*self.signal.sampling_rate/1000)  # 20 ms step
        n_per_segment = calculations.nextpow2(window_size)

        self.frqaxis, self.taxis, self.spectrogram = sig.spectrogram(x=self.signal.data,
                                                                     fs=self.signal.sampling_rate,
                                                                     nperseg=n_per_segment,
                                                                     noverlap=window_size-step_size,
                                                                     window='hamming',)
        print(f'Input data shape: {np.shape(self.signal.data)}')
        print(f'Shape (number_of_rows, number_of_columns) of the outcome spectrogram: {np.shape(self.spectrogram)}')

    def normalize_spectrogram(self):
        self.spectrogram = self.spectrogram / np.max(self.spectrogram)

    def plot_spectrogram(self):
        # assert self.spectrogram is None, 'Spectrogram has not been calculated yet'
        plt.imshow(self.spectrogram, aspect='auto', extent=[self.max_time//2, self.max_time,
                                                            0, self.signal.sampling_rate])
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

    # Creating and plotting spectrogram
    spec = Spectrogram(sig, max_t)
    spec.calculate_spectrogram()
    spec.normalize_spectrogram()
    spec.plot_spectrogram()
