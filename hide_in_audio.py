import os
import argparse

from utils import audioread
from visualization.single_signal import Signal
from letters.short_text import Text
from visualization.spectrogram import Spectrogram


def main(arguments: argparse.Namespace):
    args_dict = vars(arguments)

    if not os.path.exists(args_dict['input']):
        raise ValueError('Given path does not exist. If default, make sure to clone the repository again.')

    input_path = args_dict['input']
    max_load_time = args_dict['max_time']

    read_samples, read_sr = audioread.read_file(input_path, max_load_time)
    sig = Signal(read_samples, read_sr)

    # Shape parameters
    start_time = args_dict['start_time']
    start_frequency = args_dict['start_frq']
    text_width = args_dict['width']
    text_height = args_dict['height']
    text_itself = args_dict['text']

    # Creating and applying text
    text = Text(sig, start_time, start_frequency, text_width, text_height, text_itself)
    text.create_shape()
    sig.apply_shape(text)

    if args_dict['output_sound']:
        print('Displaying the graph of the audio after calculations ...')
        audioread.plot_sound(sig.data, sig.sampling_rate)

    if args_dict['display']:
        print('Displaying the spectrogram of the audio after calculations ...')
        spec = Spectrogram(sig)
        spec.calculate_spectrogram()
        spec.plot_spectrogram()

    if args_dict['save']:
        path_to_save = args_dict['save']
        if os.path.exists(path_to_save) and not args_dict['force']:
            print(f'Cannot save file to the given path. File of the path {path_to_save} already exists.')
            print(f'Use --force to overwrite this file.')
        else:
            print(f'Saving file to {path_to_save} ...')
            sig.save_signal(path_to_save)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hide a text message in the given sound',
                                     epilog='Use it for fun or for serious cryptography. Enjoy.',
                                     allow_abbrev=True)

    # Arguments
    parser.add_argument('-i',
                        '--input',
                        metavar='input_path',
                        help='Input audio file path to be read.',
                        type=str,
                        default='./test_audio/grilledcheesesandwich.wav')
    parser.add_argument('-t',
                        '--text',
                        metavar='text',
                        help='Text to be hidden inside an audio file.',
                        type=str,
                        default='PASSWORD')
    parser.add_argument('-b',
                        '--start_time',
                        help='Starting time of the text (in seconds).',
                        action='store',
                        type=float,
                        metavar='start_t',
                        default=0.5)
    parser.add_argument('-f',
                        '--start_frq',
                        help='Starting frequency of the text (in Hz).',
                        action='store',
                        type=float,
                        metavar='start_frq',
                        default=8000)
    parser.add_argument('-w',
                        '--width',
                        help='Width of the text (in seconds).',
                        action='store',
                        type=float,
                        metavar='width',
                        default=8)
    parser.add_argument('-e',
                        '--height',
                        help='Height of the text (in Hz).',
                        action='store',
                        type=float,
                        metavar='height',
                        default=1000)
    parser.add_argument('-m',
                        '--max_time',
                        help='Time at which an audio file should be sliced to.',
                        action='store',
                        nargs=1,
                        type=float,
                        default=-1)
    parser.add_argument('-o',
                        '--output_sound',
                        action='store_true',
                        help='Displaying an audio graph after calculations',
                        default=False)
    parser.add_argument('-d',
                        '--display',
                        action='store_true',
                        help='Displaying a spectrogram after calculations',
                        default=False)
    parser.add_argument('--force',
                        action='store_true',
                        help='Forcing to save an audio file at the already taken name.',
                        default=False)
    parser.add_argument('-s',
                        '--save',
                        action='store',
                        help='Saving path to which an audio file with added text should be saved to',
                        nargs=1,
                        type=str)

    args = parser.parse_args()
    main(args)
