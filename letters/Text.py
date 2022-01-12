from typing import List
import numpy as np

from letters.letter import Letter


class Text:

    sound_data: np.ndarray
    starting_time: float
    starting_frq: float
    text_width: float
    text_height: float
    dictionary_path: str
    whole_text: str
    all_letters: List[Letter]

    def __init__(self, sound, start_t, start_f, width, height, text: str, dict_path: str):

        self.sound_data = sound
        self.starting_time = start_t
        self.starting_frq = start_f
        self.text_width = width
        self.text_height = height
        self.whole_text = text
        self.dictionary_path = dict_path

        number_of_letters = len(text)

        if number_of_letters:
            for i, sym in enumerate(text):
                local_width_k = i/number_of_letters
                self.all_letters.append(Letter(self.sound_data,
                                               self.starting_time * local_width_k,
                                               self.starting_frq,
                                               self.text_width / number_of_letters,
                                               self.text_height,
                                               sym))
        else:
            raise ValueError('Cannot show empty string')
