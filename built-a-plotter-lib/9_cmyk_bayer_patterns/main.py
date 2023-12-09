from gcode2dplotterart import Plotter2D
import cv2
from typing import List, Tuple
import math

# TODO - make a dictionary of primaries to other colors.

plotter = Plotter2D(
    title="CMYK Bayer Patterns",
    x_max=200,
    x_min=0,
    y_max=200,
    y_min=0,
    feed_rate=10000,
    include_comments=False,
)

LINE_WIDTH = 2.5

CYAN_LAYER = "cyan"
MAGENTA_LAYER = "magenta"
YELLOW_LAYER = "yellow"
BLACK_LAYER = "black"

color_lookup = {
    (0, 255, 255): CYAN_LAYER,
    (255, 0, 255): MAGENTA_LAYER,
    (255, 255, 0): YELLOW_LAYER,
    (0, 0, 0): BLACK_LAYER,
}

LAYERS = [CYAN_LAYER, MAGENTA_LAYER, YELLOW_LAYER, BLACK_LAYER]

for layer in LAYERS:
    plotter.add_layer(title=layer, color=layer, line_width=LINE_WIDTH)


def find_nearest_color(rgb_value: Tuple[int, int, int]):
    # Calculate the Euclidean distance to find the nearest color
    distances = {
        color: sum((a - b) ** 2 for a, b in zip(rgb_value, color))
        for color in color_lookup
    }

    nearest_color = min(distances, key=distances.get)

    return nearest_color


def map_color(sample_square, sample_size):
    if sample_square.shape != (sample_size, sample_size, 3):
        raise ValueError(
            f"Input sample must be a {sample_size}x{sample_size} square with 3 color channels."
        )
    pixel_values = [element for row in sample_square for element in row]

    nearest_colors = [find_nearest_color(pixel) for pixel in pixel_values]

    color_counts = {color: nearest_colors.count(color) for color in set(nearest_colors)}

    dominant_color = max(color_counts, key=color_counts.get)

    layer = color_lookup.get(dominant_color)

    return layer


def read_and_prep_image(
    filename: str,
) -> List[List[Tuple[int, int, int]]]:
    """
    Resize the image such that the side lengths are divisible by the number of pixels that will be used to represent each dot.(pixels_per_sample)
    """

    img = cv2.imread(filename)  # Reads in image as BGR
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print("original image shape", img.shape)

    # rounded_width = int(math.floor(img.shape[0] / side_length) * side_length)
    # rounded_height = int(math.floor(img.shape[1] / side_length) * side_length)

    # Resize expects width, height unlike in just about every other place.
    # img = cv2.resize(img, (rounded_width, rounded_height))
    # print("rounded image shape", img.shape)
    return img


def sample_img(img: List[List[Tuple[int, int, int]]], sample_size: int):
    """
    Take in an image, and return a 2D list of colors to plot as output.

    Params:
      img: The image to process
      sample_size: the number of pixels, along a side to sample. The number of pixels would then be sample_size**2.
    """

    output = []

    for starting_row in range(0, len(img), sample_size):
        output_row = []
        for starting_col in range(0, len(img[0]), sample_size):
            img_section = img[
                starting_row : starting_row + sample_size,
                starting_col : starting_col + sample_size,
            ]
            result = map_color(img_section, sample_size)
            output_row.append(result)
        output.append(output_row)

    return output


def main():
    circle_diameter = 10

    img = read_and_prep_image("./squares.png")
    sampled_img = sample_img(img, sample_size=1)

    for row_index, row in enumerate(sampled_img):
        for col_index, color in enumerate(row):
            total_rows = len(sampled_img)
            x_center = col_index * circle_diameter + circle_diameter
            y_center = (total_rows - row_index) * circle_diameter + circle_diameter

            plotter.layers[color].add_circle(
                x_center=x_center,
                y_center=y_center,
                radius=circle_diameter / 2 - circle_diameter * 0.15,
            )
    plotter.preview()


if __name__ == "__main__":
    main()
