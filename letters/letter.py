from typing import List, NoReturn
import yaml

from letters.shape import Shape, Curve, HorizontalLine, VerticalLine


class Letter(Shape):
    """A class which represents a single letter

    Attributes
    ----------
    all_figures : List[Shape]
        a list of objects of the Shape class, each representing single shape
    dictionary_path : str
        a path to the .YAML file which consist of the parameters for each shape of the letter
    dictionary_data : dict
        data returned by the yaml.safe_load() function
    symbol : str
        a character to be created

    Methods
    -------
    create_shape()
        Recalculates the shape position and creates each shape of the letter
    _recalculate_position(shape: Shape)
        Recalculates the position of the shape of the letter based on the relative position in the letter
    """

    def __init__(self, sound, start_t, start_f, width, height, symbol: str):
        """
        Parameters
        ----------
        sound
            a base sound as a Signal class object, used as a template for calculations
        start_t
            a floating point number representing the beginning of the letter - left border [in seconds]
        start_f
            a floating point number representing the beginning of the letter - bottom border [in HZ]
        width
            a floating point number representing the width of the letter [in seconds]
        height
            a floating point number representing the height of the letter [in Hz]
        symbol : str
            a string representing a character to create

        Raises
        ------
        NotImplementedError
            If the given character has not been implemented in the YAML dictionary
        """

        super().__init__(sound, start_t, start_f, width, height)

        self.all_figures: List[Shape] = []
        self.dictionary_path: str = './letters/dictionary.yaml'
        self.dictionary_data: dict = {}
        self.symbol: str = symbol

        # Loading dictionary
        with open(self.dictionary_path, "r") as stream:
            try:
                self.dictionary_data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        if symbol not in self.dictionary_data['All_Letters']:
            raise NotImplementedError(f"Cannot create '{symbol}' because it is not implemented yet.")
        else:
            for shape in self.dictionary_data[symbol]:
                if shape == 'Curve':
                    for iteration in self.dictionary_data[symbol][shape]:
                        parameters = self.dictionary_data[symbol][shape][iteration]
                        self.all_figures.append(Curve(sound,
                                                      width * parameters[0],
                                                      height * parameters[1],
                                                      width * parameters[2] * 0.95,
                                                      height * parameters[3],
                                                      desc=parameters[4]))
                if shape == 'Horizontal':
                    for iteration in self.dictionary_data[symbol][shape]:
                        parameters = self.dictionary_data[symbol][shape][iteration]
                        self.all_figures.append(HorizontalLine(sound,
                                                               width * parameters[0],
                                                               height * parameters[1],
                                                               width * parameters[2] * 0.95,
                                                               height * parameters[3]))
                if shape == 'Vertical':
                    for iteration in self.dictionary_data[symbol][shape]:
                        parameters = self.dictionary_data[symbol][shape][iteration]
                        self.all_figures.append(VerticalLine(sound,
                                                             width * parameters[0],
                                                             height * parameters[1],
                                                             width * parameters[2] * 0.95,
                                                             height * parameters[3]))

    def create_shape(self) -> NoReturn:
        """Recalculates position, creates a shape, combines new shape with base figure"""

        for shape in self.all_figures:
            shape = self._recalculate_position(shape)
            shape.create_shape()
            self._combine_figures(shape.figure, shape.start_point_t)

    def _recalculate_position(self, new_shape: Shape):
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
            if time starting point after recalculation is to big for new figure to fit the range
        ValueError
            if frequency starting point after recalculation is to big for new figure to fit the range
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
