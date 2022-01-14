from typing import NoReturn

import numpy as np
import librosa
import matplotlib.pyplot as plt


def read_file(path_to_file: str, time: float):
    """Function used to read data from the audio file

    Parameters
    ----------
    path_to_file : str
        a path to the file from which to read the data
    time : float
        time to slice loaded file

    Returns
    -------
    samples
        samples of audio data
    sampling_frq
        self-explanatory
    """

    samples, sampling_frq = librosa.load(path_to_file)

    if time < 0:
        print('Max time not given (or negative). Loading entire audio file.')
    else:
        max_samples = int(sampling_frq * time)
        if len(samples) >= max_samples:
            # The signal is cropped to the range of [0: given_time]
            samples = samples[0:max_samples]
        else:
            raise ValueError('Signal is not long enough for the given maximum time value')
    return samples, sampling_frq


def plot_sound(amplitudes: np.ndarray, sampling_frequency: float) -> NoReturn:
    """Function used to plot the sound in time domain using pyplot module

    Parameters
    ----------
    amplitudes : np.ndarray
        samples of the audio file
    sampling_frequency : float
        self-explanatory

    Raises
    ------
    AssertionError
        Size of time domain array does not match the number of samples
    """

    n = len(amplitudes)  # number of samples
    time_step = 1/sampling_frequency
    time_domain = [i*time_step for i in range(n)]

    assert n == len(time_domain), 'Size of time domain array does not match the number of samples'

    plt.plot(time_domain, amplitudes)
    plt.title('Given audio signal in time domain')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitudes')
    plt.grid(visible=True)
    plt.show()


if __name__ == '__main__':
    pass
