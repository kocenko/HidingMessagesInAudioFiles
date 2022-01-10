import numpy as np
from scipy.signal import chirp

from utils.audioread import plot_sound


class Shape:
    curve = None

    def __init__(self, width, length, start, sound):
        self.width = width  # In sec
        self.length = length  # In Hz
        self.start_point = start  # In sec
        self.template = sound

    def create_curve(self):
        fs = self.template.sampling_rate
        t = np.arange(0, self.width * fs - 1, 1) / fs

        # For now in the middle of the range
        f0 = 1
        f1 = 15
        t1 = self.width

        self.curve = chirp(t=t, f0=f0, f1=f1, t1=t1, method='linear')

        plot_sound(self.curve, fs)

        print(f'SHAPE --- Curve size: {len(self.curve)}')
