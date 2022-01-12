from typing import List, NoReturn

from letters.shape import Shape, Curve, HorizontalLine, VerticalLine


class Letter(Shape):

    all_figures: List[Shape]

    def __init__(self, sound, start_t, start_f, width, height, symbol: str):
        super().__init__(sound, start_t, start_f, width, height)

        self.all_figures = []
        self.symbol = symbol

        if symbol == 'A':
            self.all_figures.append(Curve(sound, 0, 0, width/2, height))
            self.all_figures.append(Curve(sound, width/2, 0, width/2, height, desc=True))
            self.all_figures.append(HorizontalLine(sound, width/4, height/2, width/2, 0))
        elif symbol == 'B':
            self.all_figures.append(HorizontalLine(sound, 0, height, width, 0))
            self.all_figures.append(HorizontalLine(sound, 0, 0, width, 0))
            self.all_figures.append(HorizontalLine(sound, 0, height/2, width, 0))
            self.all_figures.append(VerticalLine(sound, 0, 0, 0.02, height))
            self.all_figures.append(VerticalLine(sound, width - 0.02, 0, 0.02, height))
        elif symbol == 'C':
            self.all_figures.append(HorizontalLine(sound, 0, height, width, 0))
            self.all_figures.append(HorizontalLine(sound, 0, 0, width, 0))
            self.all_figures.append(VerticalLine(sound, 0, 0, 0.02, height))
        elif symbol == 'G':
            self.all_figures.append(HorizontalLine(sound, 0, height, width, 0))
            self.all_figures.append(HorizontalLine(sound, 0, 0, width, 0))
            self.all_figures.append(HorizontalLine(sound, width/2, height/2, width/2, 0))
            self.all_figures.append(VerticalLine(sound, 0, 0, 0.02, height))
            self.all_figures.append(VerticalLine(sound, width-0.02, 0, 0.02, height/2))
        elif symbol == 'T':
            self.all_figures.append(HorizontalLine(sound, 0, height, width, 0))
            self.all_figures.append(VerticalLine(sound, width/2, 0, 0.02, height))
        else:
            raise NotImplementedError

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
