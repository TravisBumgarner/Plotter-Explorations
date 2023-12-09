from gcode2dplotterart import Plotter2D
import cv2
from typing import List, Tuple
from random import shuffle
import time

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


# Ideally percentages are divisible by 25, so that the number of points can be divided into quarters.
color_name_to_cyan_percentage = {
    "red": {"cyan": 0, "magenta": 50, "yellow": 50, "black": 0},
    "orange": {"cyan": 0, "magenta": 50, "yellow": 50, "black": 0},
    "yellow": {"cyan": 0, "magenta": 0, "yellow": 100, "black": 0},
    "green": {"cyan": 50, "magenta": 0, "yellow": 50, "black": 0},
    "blue": {"cyan": 50, "magenta": 50, "yellow": 0, "black": 0},
    "cyan": {"cyan": 100, "magenta": 0, "yellow": 0, "black": 0},
    "magenta": {"cyan": 0, "magenta": 100, "yellow": 0, "black": 0},
    "black": {"cyan": 0, "magenta": 0, "yellow": 0, "black": 100},
    "white": {"cyan": 0, "magenta": 0, "yellow": 0, "black": 0},
}

rgb_to_color_name = {
    (255, 0, 0): "red",
    (255, 165, 0): "orange",
    (255, 255, 0): "yellow",
    (0, 255, 0): "green",
    (0, 0, 255): "blue",
    (0, 255, 255): "cyan",
    (255, 0, 255): "magenta",
    (0, 0, 0): "black",
    (255, 255, 255): "white",
}

if set(color_name_to_cyan_percentage.keys()) != set(rgb_to_color_name.values()):
    raise ValueError(
        "The color names in color_name_to_cyan_percentage must match the color names in rgb_to_color_name."
    )

LAYERS = [CYAN_LAYER, MAGENTA_LAYER, YELLOW_LAYER, BLACK_LAYER]

for layer in LAYERS:
    plotter.add_layer(title=layer, color=layer, line_width=LINE_WIDTH)


def find_nearest_color(rgb_value: Tuple[int, int, int]):
    # Calculate the Euclidean distance to find the nearest color
    distances = {
        color: sum((a - b) ** 2 for a, b in zip(rgb_value, color))
        for color in rgb_to_color_name
    }

    nearest_color = min(distances, key=distances.get)

    return nearest_color


def map_color(sample_square, pixels_per_sample_side):
    if sample_square.shape != (pixels_per_sample_side, pixels_per_sample_side, 3):
        raise ValueError(
            f"Input sample must be a {pixels_per_sample_side}x{pixels_per_sample_side} square with 3 color channels."
        )
    pixel_values = [element for row in sample_square for element in row]

    nearest_colors = [find_nearest_color(pixel) for pixel in pixel_values]

    color_counts = {color: nearest_colors.count(color) for color in set(nearest_colors)}

    dominant_color = max(color_counts, key=color_counts.get)

    color_name = rgb_to_color_name.get(dominant_color)

    return color_name


# def map_color(sample_square, pixels_per_sample_side):
#     if sample_square.shape != (pixels_per_sample_side, pixels_per_sample_side, 3):
#         raise ValueError(
#             f"Input sample must be a {pixels_per_sample_side}x{pixels_per_sample_side} square with 3 color channels."
#         )

#     # Reshape the sample_square into a 2D array
#     reshaped_sample = sample_square.reshape(-1, 3)

#     # Find the nearest color for each pixel using NumPy
#     nearest_colors = np.apply_along_axis(find_nearest_color, 1, reshaped_sample)

#     # Count occurrences of each color in the sample using NumPy
#     unique_colors, counts = np.unique(nearest_colors, axis=0, return_counts=True)

#     # Get the color with the highest count
#     dominant_color = unique_colors[np.argmax(counts)]

#     # Convert to a regular Python list before creating a tuple
#     dominant_color_list = (
#         dominant_color.tolist()
#         if isinstance(dominant_color, np.ndarray)
#         else dominant_color
#     )

#     color_name = rgb_to_color_name.get(tuple(dominant_color_list))

#     return color_name


def read_and_prep_image(
    filename: str,
) -> List[List[Tuple[int, int, int]]]:
    """
    Resize the image such that the side lengths are divisible by the number of pixels that will be used to represent each dot.(pixels_per_sample)
    """

    img = cv2.imread(filename)  # Reads in image as BGR
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # print("original image shape", img.shape)

    # rounded_width = int(math.floor(img.shape[0] / side_length) * side_length)
    # rounded_height = int(math.floor(img.shape[1] / side_length) * side_length)

    # Resize expects width, height unlike in just about every other place.
    # img = cv2.resize(img, (rounded_width, rounded_height))
    # print("rounded image shape", img.shape)
    return img


def image_to_cmyk_color_ratios(
    img: List[List[Tuple[int, int, int]]], pixels_per_sample_side: int
):
    """
    Take in an image, and return a 2D list of colors to plot as output.

    Params:
      img: The image to process
      pixels_per_sample_side: the number of pixels, along a side to sample. The number of pixels would then be pixels_per_sample_side**2.
    """

    output = []

    for starting_row in range(0, len(img), pixels_per_sample_side):
        output_row = []
        for starting_col in range(0, len(img[0]), pixels_per_sample_side):
            img_section = img[
                starting_row : starting_row + pixels_per_sample_side,
                starting_col : starting_col + pixels_per_sample_side,
            ]
            result = map_color(img_section, pixels_per_sample_side)
            cmyk_ratio = color_name_to_cyan_percentage.get(result)
            output_row.append(cmyk_ratio)
        output.append(output_row)

    return output


def plot_points_per_cmyk_ratio(
    cmyk_ratio,
    x_start_mm,
    y_start_mm,
    mm_per_section_side,
    points_per_sample_side,
):
    points = []
    # print("sampling", points_per_sample_side**2)
    for color, percentage in cmyk_ratio.items():
        num_points = int(percentage / 100 * points_per_sample_side**2)
        # print("\t", color, num_points)
        for i in range(num_points):
            points.append(color)

    # Need to handle the situation where the number of points is less than the number of points per sample side.
    # One such way this occurs is if the points_per_sample_side is odd.
    filtered_dict = {k: v for k, v in cmyk_ratio.items() if v != 0}
    # Sort the dictionary by values in descending order
    sorted_dict = list(
        dict(
            sorted(filtered_dict.items(), key=lambda item: item[1], reverse=True)
        ).keys()
    )

    current_index = 0
    while len(points) < points_per_sample_side**2:
        points.append(sorted_dict[current_index % len(sorted_dict)])
        current_index += 1

    shuffle(points)

    x_spacing = mm_per_section_side / points_per_sample_side
    y_spacing = mm_per_section_side / points_per_sample_side

    for i in range(points_per_sample_side):
        for j in range(points_per_sample_side):
            x = x_start_mm + i * x_spacing
            y = y_start_mm - j * y_spacing
            plot_color = points.pop()

            plotter.layers[plot_color].add_point(
                x=x,
                y=y,
            )


def main():
    mm_per_section_side = 10
    points_per_sample_side = 7
    pixels_per_sample_side = 1

    img = read_and_prep_image("./squares.png")

    cmyk_color_ratios = image_to_cmyk_color_ratios(
        img, pixels_per_sample_side=pixels_per_sample_side
    )

    for row_index, row in enumerate(cmyk_color_ratios):
        for col_index, cmyk_ratio in enumerate(row):
            total_rows = len(cmyk_color_ratios)
            x_start_mm = col_index * mm_per_section_side + mm_per_section_side
            y_start_mm = (
                total_rows - row_index
            ) * mm_per_section_side + mm_per_section_side

            plot_points_per_cmyk_ratio(
                cmyk_ratio=cmyk_ratio,
                x_start_mm=x_start_mm,
                y_start_mm=y_start_mm,
                mm_per_section_side=mm_per_section_side,
                points_per_sample_side=points_per_sample_side,
            )
    plotter.preview()


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    # print(f"Total time: {end_time - start_time}")
