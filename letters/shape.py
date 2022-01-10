from typing import NoReturn
import numpy as np
from scipy.signal import chirp


class Shape:
    curve = None

    def __init__(self, width, length, start, sound):
        self.width = width  # In sec
        self.length = length  # In Hz
        self.start_point = start  # In sec
        self.template = sound

    def create_curve(self) -> NoReturn:
        fs = self.template.sampling_rate
        t = np.arange(0, self.width * fs - 1, 1) / fs

        # For now in the middle of the range
        f0 = fs/8
        f1 = 3*fs/8
        t1 = self.width

        # Creating chirp signal
        self.curve = chirp(t=t, f0=f0, f1=f1, t1=t1, method='linear')

        # Scaling chirp signal
        scale = np.mean(np.abs(self.template.data)) / np.mean(np.abs(self.curve))
        self.curve = self.curve * scale
