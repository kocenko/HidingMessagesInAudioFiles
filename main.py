from utils import audioread
from visualization.single_signal import Signal
from letters.short_text import Text
from visualization.spectrogram import Spectrogram

# Initial parameters
path = './test_audio/grilledcheesesandwich.wav'
max_t = 40

# Creating signal
read_samples, read_sr = audioread.read_file(path, max_t)
sig = Signal(read_samples, read_sr)

# Creating shape
letter_width = max_t/5
letter_height = 1000
letter_start_t = 0.5
letter_start_f = 8000

# Curve(sig, letter_start_t, letter_start_f, letter_width, letter_height)
# letter = Letter(sig, letter_start_t, letter_start_f, letter_width, letter_height, 'A')
# letter.create_shape()
letter = Text(sig, letter_start_t, letter_start_f, letter_width, letter_height, 'ZYCIE BEZ')
letter2 = Text(sig, letter_start_t, letter_start_f, letter_width, letter_height, 'NIC')
letter.create_shape()
letter2.create_shape()
sig.apply_shape(letter)
# sig.apply_shape(letter2)

audioread.plot_sound(sig.data, sig.sampling_rate)

# Creating and plotting spectrogram after
spec = Spectrogram(sig)
spec.calculate_spectrogram()
spec.normalize_spectrogram()
spec.plot_spectrogram()

sig.save_signal('wynik.wav')