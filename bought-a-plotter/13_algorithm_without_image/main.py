from Image import Image
from utils import folder_setup
from Plotter import Plotter
import image_algorithms
import math_algorithms

def main_with_image(filename, output_colors, x_offset, y_offset):
    folder_setup()
    plotter = Plotter(units="mm", x_min = 0, x_max = 280, y_min = -200, y_max = 0, feed_rate=10000)

    image = Image(filename)
    image.prepare_for_bucket_algorithm(should_resize=False, should_rotate=True)
    image.apply_bucket_algorithm(method='bucket_pixels_evenly_by_output_colors', output_colors=output_colors)
    image_algorithms.horizontal_lines_algorithm(plotter, output_filename=filename, processed_image=image.image, output_colors=output_colors, x_offset=x_offset, y_offset=y_offset)

# main_with_image(
#     filename='test.png',
#     output_colors=[ 'red', 'gold', 'blue'],
#     x_offset=75,
#     y_offset=0,
# )


def main_with_math(output_colors, x_offset, y_offset):
    folder_setup()
    plotter = Plotter(units="mm", x_min = 0, x_max = 120, y_min = -120, y_max = 0, feed_rate=10000)
    math_algorithms.wander(plotter=plotter, filename_prefix='wander', output_colors=output_colors, x_offset=x_offset, y_offset=y_offset)

main_with_math(
    output_colors=[ 'blue1', 'blue2', 'blue3', 'blue4'],
    x_offset=0,
    y_offset=0,

)

