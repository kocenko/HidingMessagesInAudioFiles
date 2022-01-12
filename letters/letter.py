from typing import List, NoReturn
import matplotlib.pyplot as plt

from letters.shape import Shape, Curve, HorizontalLine, VerticalLine


class Letter(Shape):

    all_figures: List[Shape] = []

    def __init__(self, sound, start_t, start_f, width, height, symbol: str):
        super().__init__(sound, start_t, start_f, width, height)

        if symbol == 'A':
            self.all_figures.append(Curve(sound, 0, 0, width/2, height))
            self.all_figures.append(Curve(sound, width/2, 0, width/2, height, desc=True))
            self.all_figures.append(HorizontalLine(sound, width/4, height/2, width/2, 0))
            self.all_figures.append(HorizontalLine(sound, 0, height, width, 0))
            self.all_figures.append(VerticalLine(sound, width/2-0.02, 0, 0.02, height))
        elif symbol == 'G':
            self.all_figures.append(HorizontalLine(sound, 0, height, width, 0))
            self.all_figures.append(HorizontalLine(sound, 0, 0, width, 0))
            self.all_figures.append(HorizontalLine(sound, width/2, height/2, width/2, 0))
            self.all_figures.append(VerticalLine(sound, 0, 0, 0.02, height))
            self.all_figures.append(VerticalLine(sound, width-0.02, 0, 0.02, height/2))
        else:
            raise NotImplementedError

    def create_shape(self) -> NoReturn:
        for i, shape in enumerate(self.all_figures):
            shape = self._recalculate_position(shape)
            shape.create_shape()

            plt.plot(shape.figure)
            plt.title(f'Class: Letter, Method: create_shape, Figure: {i}')
            plt.show()

            self._combine_figures(shape.figure, shape.start_point_t)

        self._scale_figure()

    def _recalculate_position(self, new_shape: Shape) -> Shape:
        precision = -1.e-3

        temp_shape = new_shape
        if new_shape.start_point_t < 0:
            raise ValueError('Time placement cannot be negative')
        if new_shape.start_point_f < 0:
            raise ValueError('Frequency placement cannot be negative')

        temp_shape.start_point_t = self.start_point_t + new_shape.start_point_t
        if (self.start_point_t + self.width) - (temp_shape.start_point_t + temp_shape.width) < precision:
            raise ValueError('Cannot create the shape: placement + width exceeds the maximum size')

        temp_shape.start_point_f = self.start_point_f + new_shape.start_point_f
        if (self.start_point_f + self.height) - (temp_shape.start_point_f + temp_shape.height) < precision:
            raise ValueError('Cannot create the shape: placement + width exceeds the maximum size')

        return temp_shape
