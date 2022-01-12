from typing import List, NoReturn
# import matplotlib.pyplot as plt

from letters.shape import Shape
from letters.letter import Letter


class Text(Shape):

    max_number_of_letters: int = 6
    dictionary_path: str
    whole_text: str
    all_letters: List[Letter]

    def __init__(self, sound, start_t, start_f, width, height, text: str):
        super().__init__(sound, start_t, start_f, width, height)

        self.all_letters = []
        self.whole_text = text

        number_of_letters = len(self.whole_text)
        if number_of_letters / width > self.max_number_of_letters:
            raise ValueError('Letters cannot be as densely packed')
        if number_of_letters:
            for i, sym in enumerate(text):
                local_width_k = i / number_of_letters
                self.all_letters.append(Letter(self.template,
                                               local_width_k * self.width,
                                               0,
                                               self.width / number_of_letters,
                                               self.height,
                                               sym))
        else:
            raise ValueError('Cannot show empty string')

    def create_shape(self) -> NoReturn:
        for letter in self.all_letters:

            # print(f'\n----------------------------\n'
            #       f'CREATING LETTER {letter.symbol}\n')

            letter = self._recalculate_position(letter)
            letter.create_shape()
            self._combine_figures(letter.figure, letter.start_point_t)

            # print(f'FINISHED CREATING LETTER {letter.symbol}\n'
            #       f'------------------------------\n')

        # plt.plot(self.figure)
        # plt.title('Letters figure')
        # plt.show()

    def _recalculate_position(self, new_shape):
        precision = -1.e-9

        if new_shape.start_point_t < 0:
            raise ValueError('Time placement cannot be negative')
        if new_shape.start_point_f < 0:
            raise ValueError('Frequency placement cannot be negative')

        new_shape.start_point_t = self.start_point_t + new_shape.start_point_t
        if (self.start_point_t + self.width) - (new_shape.start_point_t + new_shape.width) < precision:
            raise ValueError('Cannot create the shape: placement + width exceeds the maximum size')

        new_shape.start_point_f = self.start_point_f + new_shape.start_point_f
        if (self.start_point_f + self.height) - (new_shape.start_point_f + new_shape.height) < precision:
            raise ValueError('Cannot create the shape: placement + width exceeds the maximum size')

        return new_shape
