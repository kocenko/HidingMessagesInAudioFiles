import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt

from utils import audioread, calculations


class Spectrogram:
    sampling_rate: float
    max_time: float
    data: np.ndarray
    taxis: np.ndarray = None
    frqaxis: np.ndarray = None
    spectrogram: np.ndarray = None

    def __init__(self, audio_path, t):
        self.max_time = t
        samples, fs = audioread.read_file(audio_path, self.max_time)
        self.data = samples
        self.sampling_rate = fs

    def calculate_spectrogram(self):
        # window_size = np.ceil(100*self.sampling_rate/1000)  # 100 ms window
        # step_size = np.ceil(20*self.sampling_rate/1000)  # 20 ms step
        # n_per_segment = calculations.nextpow2(window_size)
        # print(f'NperSeg: {n_per_segment}')
        self.frqaxis, self.taxis, self.spectrogram = sig.spectrogram(x=self.data,
                                                                     fs=self.sampling_rate)
        print(f'Input data shape: {np.shape(self.data)}')
        print(f'Shape (number_of_rows, number_of_columns) of the outcome spectrogram: {np.shape(self.spectrogram)}')

    def normalize_spectrogram(self):
        self.spectrogram = self.spectrogram / np.max(self.spectrogram)

    def plot_spectrogram(self):
        # assert self.spectrogram is None, 'Spectrogram has not been calculated yet'
        plt.imshow(self.spectrogram, aspect='auto', extent=[self.max_time//2, self.max_time,
                                                            0, self.sampling_rate])
        plt.title('Given audio signal in frequency and time domain')
        plt.xlabel('Time [s]')
        plt.ylabel('Frequencies [Hz]')
        plt.show()


if __name__ == '__main__':
    path = '../test_audio/grilledcheesesandwich.wav'
    max_t = 4
    spec = Spectrogram(path, max_t)
    spec.calculate_spectrogram()
    spec.normalize_spectrogram()
    spec.plot_spectrogram()
