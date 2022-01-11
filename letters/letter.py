from typing import List, NoReturn
import matplotlib.pyplot as plt

from letters.shape import Shape, Curve, HorizontalLine, VerticalLine


class Letter(Shape):

    all_figures: List[Shape] = []

    def __init__(self, sound, start_t, start_f, width, height, symbol: str, x_dir: bool = True, y_dir: bool = True):
        super().__init__(sound, start_t, start_f, width, x_dir)

        self.y_direction = y_dir

        if symbol == 'A':
            self.all_figures.append(Curve(sound, start_t, start_f, width/2, height))
            self.all_figures.append(Curve(sound, start_t+width/2, start_f, width/2, height, x_dir=False, desc=True))
            self.all_figures.append(HorizontalLine(sound, start_t, start_f+height/2, width))
            self.all_figures.append(VerticalLine(sound, start_t+width/2, start_f, 0.02, height))
        else:
            raise NotImplementedError

    def create_shape(self) -> NoReturn:
        for i, shape in enumerate(self.all_figures):
            shape.create_shape()
            print(f'\nClass: Letter, Method: create_shape, given shape length: {shape.figure.size}\n'
                  f'Expected length {self.figure.size}\n')

            plt.plot(shape.figure)
            plt.title(f'Class: Letter, Method: create_shape, Figure: {i}')
            plt.show()

            self._combine_figures(shape.figure, shape.x_direction)

        self._scale_figure()
