from typing import List, NoReturn
import yaml

from letters.shape import Shape, Curve, HorizontalLine, VerticalLine


class Letter(Shape):

    all_figures: List[Shape]
    dictionary_path: str = '../letters/dictionary.yaml'
    dictionary_data = None

    def __init__(self, sound, start_t, start_f, width, height, symbol: str):
        super().__init__(sound, start_t, start_f, width, height)

        self.all_figures = []
        self.symbol = symbol

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
                        print(f'{shape} options: {self.dictionary_data[symbol][shape][iteration]}')
                        self.all_figures.append(Curve(sound,
                                                      width * parameters[0],
                                                      height * parameters[1],
                                                      width * parameters[2] * 0.95,
                                                      height * parameters[3],
                                                      desc=parameters[4]))
                if shape == 'Horizontal':
                    for iteration in self.dictionary_data[symbol][shape]:
                        parameters = self.dictionary_data[symbol][shape][iteration]
                        print(f'{shape} options: {self.dictionary_data[symbol][shape][iteration]}')
                        self.all_figures.append(HorizontalLine(sound,
                                                               width * parameters[0],
                                                               height * parameters[1],
                                                               width * parameters[2] * 0.95,
                                                               height * parameters[3]))
                if shape == 'Vertical':
                    for iteration in self.dictionary_data[symbol][shape]:
                        parameters = self.dictionary_data[symbol][shape][iteration]
                        print(f'{shape} options: {self.dictionary_data[symbol][shape][iteration]}')
                        self.all_figures.append(VerticalLine(sound,
                                                             width * parameters[0],
                                                             height * parameters[1],
                                                             width * parameters[2] * 0.95,
                                                             height * parameters[3]))

    def create_shape(self) -> NoReturn:
        for i, shape in enumerate(self.all_figures):
            shape = self._recalculate_position(shape)
            shape.create_shape()

            # plt.plot(shape.figure)
            # plt.title(f'Class: Letter, Method: create_shape, Figure: {i}')
            # plt.show()

            self._combine_figures(shape.figure, shape.start_point_t)

    def _recalculate_position(self, new_shape):
        precision = -1.e-9

        # print(f'You got into {new_shape.id_name} recalculation\n'
        #       f'Position before calc: {new_shape.start_point_t}')

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

        # print(f'And after calc: {new_shape.start_point_t}\n')

        return new_shape
