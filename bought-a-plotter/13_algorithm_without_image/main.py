from Image import Image
from utils import folder_setup
from image_algorithms import horizontal_lines_algorithm

def main(filename, output_colors, x_offset, y_offset):
    folder_setup()

    image = Image(filename)
    image.prepare_for_bucket_algorithm(should_resize=False, should_rotate=True)
    image.apply_bucket_algorithm(method='bucket_pixels_evenly_by_output_colors', output_colors=output_colors)
    horizontal_lines_algorithm(output_filename=filename, processed_image=image.image, output_colors=output_colors, x_offset=x_offset, y_offset=y_offset)

main(
    filename='test.png',
    output_colors=[ 'red', 'gold', 'blue'],
    x_offset=75,
    y_offset=0,
)


