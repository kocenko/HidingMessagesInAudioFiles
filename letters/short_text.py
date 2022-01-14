from typing import List, NoReturn

from letters.shape import Shape
from letters.letter import Letter


class Text(Shape):
    """A class which represents a text

    Attributes
    ----------
    max_number_of_letters : int
        integer value representing a number of letters that can be packed in certain range
    all_letters : List[Letter]
        list of objects of Letter class each representing single letter
    space_usage
        constant value representing how much space will be taken from the space reserved for the letter [in percent]
    whole_text : str
        a string to be created on the sound file

    Methods
    -------
    create_shape()
        Recalculates the letter position and creates a letter
    _recalculate_position(shape: Shape)
        Recalculates the position of the letter based on the relative position in the text
    """

    def __init__(self, sound, start_t, start_f, width, height, text: str):
        """
        Parameters
        ----------
        sound
            a base sound as a Signal class object, used as a template for calculations
        start_t
            a floating point number representing the beginning of the text - left border [in seconds]
        start_f
            a floating point number representing the beginning of the text - bottom border [in HZ]
        width
            a floating point number representing the width of the text [in seconds]
        height
            a floating point number representing the height of the text [in Hz]
        text : str
            a string representing a text to create

        Raises
        ------
        ValueError
            Letters are very densely packed - according to the max_number_of_letters value
        ValueError
            Given string is empty
        """

        super().__init__(sound, start_t, start_f, width, height)

        self.space_usage = 80/100
        self.max_number_of_letters: int = 6
        self.all_letters: List[Letter] = []
        self.whole_text: str = text

        number_of_letters = len(self.whole_text)
        if number_of_letters / width > self.max_number_of_letters:
            raise ValueError('Letters cannot be as densely packed')
        if number_of_letters:
            for i, sym in enumerate(text):
                if sym != ' ':
                    local_width_k = i / number_of_letters
                    self.all_letters.append(Letter(self.template,
                                                   local_width_k * self.width,
                                                   0,
                                                   self.width * self.space_usage / number_of_letters,
                                                   self.height,
                                                   sym))
        else:
            raise ValueError('Cannot show empty string')

    def create_shape(self) -> NoReturn:
        """Recalculates position, creates a letter, combines new letter with whole text"""

        for letter in self.all_letters:
            letter = self._recalculate_position(letter)
            letter.create_shape()
            self._combine_figures(letter.figure, letter.start_point_t)

    def _recalculate_position(self, new_shape):
        """Recalculates position of the new shape in respect to the base figure

        Parameters
        ----------
        new_shape : Shape
            new shape which starting points are being recalculated

        Returns
        -------
        new_shape : Shape
            new shape after recalculations

        Raises
        ------
        ValueError
            if time starting point of the new shape is negative
        ValueError
            if frequency starting point of the new shape is negative
        ValueError
            if time starting point after recalculation is to big for new figure to fit in the range
        ValueError
            if frequency starting point after recalculation is to big for new figure to fit in the range
        """

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
