import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

from utils import calculations
from visualization.single_signal import Signal


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
    pass
