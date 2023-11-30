from gcode2dplotterart import Plotter2D
import cv2

from typing import List
import math


LINE_WIDTH = 0.2
LAYER_BLACK = {"title": "black", "color": "black", "line_width": LINE_WIDTH}

plotter = Plotter2D(
    title="Halftone",
    x_min=0,
    x_max=250,
    y_min=0,
    y_max=180,
    feed_rate=10000,
)

plotter.add_layer(**LAYER_BLACK)


def read_and_prep_image(filename: str, side_length: float) -> List[List[int]]:
    """
    Resize the image such that the side lengths are divisible by the number of pixels that will be used to represent each dot.(pixels_per_sample)
    """

    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("original image shape", img.shape)

    rounded_width = int(math.floor(img.shape[0] / side_length) * side_length)
    rounded_height = int(math.floor(img.shape[1] / side_length) * side_length)

    # Resize expects width, height unlike in just about every other place.
    img = cv2.resize(img, (rounded_width, rounded_height))
    print("rounded image shape", img.shape)
    return img


PIXELS_PER_SAMPLE = 100

# This calculation can be tweaked. The buckets don't need to be evenly distributed.
# TODO - Research those crazy curves for rates of change? Simples rate of change could be linear but could use more fancy equations.
LUMINOSITY_THRESHOLD__TO_DOT_RADIUS_MAPPING = {
    0: 0,
    50: LINE_WIDTH,
    100: LINE_WIDTH * 2,
    150: LINE_WIDTH * 3,
    200: LINE_WIDTH * 4,
    255: LINE_WIDTH * 5,
}

PADDING = 2
max_circle_radius_with_padding = (
    sorted(LUMINOSITY_THRESHOLD__TO_DOT_RADIUS_MAPPING.values(), reverse=True)[0]
    + PADDING
)

# PIXELS_PER_SAMPLE has been lost and is now unhelpful
img = read_and_prep_image("./test.png", side_length=PIXELS_PER_SAMPLE)

# Subtract, an arbitrary amount, so that circles at edge of plotter are not out of bounds.
plotter_circles_per_row = math.floor(plotter.width / (max_circle_radius_with_padding)) - 2
plotter_circles_per_column = math.floor(plotter.height / (max_circle_radius_with_padding)) - 2
print("plotter_circles_per_row", plotter_circles_per_row)
print("plotter_circles_per_column", plotter_circles_per_column)

image_rows, image_columns = img.shape

pixels_per_sample_row = math.floor(image_rows / plotter_circles_per_row)
pixels_per_sample_column = math.floor(image_columns / plotter_circles_per_column)


rows, columns = img.shape
print("image rows", rows, "columns", columns)


def calculate_radius(
    img, start_row, start_column, pixels_per_sample_row, pixels_per_sample_column
):
    total = 0

    for row in range(start_row, start_row + pixels_per_sample_row):
        for col in range(start_column, start_column + pixels_per_sample_column):
            total += img[row][col]

    average = total / (pixels_per_sample_column * pixels_per_sample_row)

    for (
        threshold,
        new_radius,
    ) in LUMINOSITY_THRESHOLD__TO_DOT_RADIUS_MAPPING.items():
        radius = new_radius
        if average < threshold:
            break
    return radius


start_row = 0
start_column = 0

output = []
while start_row < rows:
    output_row = []
    while start_column < columns:
        # print(start_column, start_row)
        try:
            radius = calculate_radius(
                img,
                start_row=start_row,
                start_column=start_column,
                pixels_per_sample_row=pixels_per_sample_row,
                pixels_per_sample_column=pixels_per_sample_column,
            )
            output_row.append(radius)
        except IndexError:
            # This try/except will probably fail towards to edges of the image. Ignoring for now, could be improved to handle that situation. 
            print("Missing points")
            output_row.append(0)

        start_column += pixels_per_sample_column
    
    start_row += pixels_per_sample_row
    start_column = 0
    output.append(output_row)
    output_row = []

for row_index, row in enumerate(output):
    for col_index, radius in enumerate(row):
        if radius == 0:
            continue
        # Add 1 to offset so that first row and column aren't outside of bounds of plotter
        plotter.layers[LAYER_BLACK["title"]].add_circle(
            x_center=(row_index + 1) * max_circle_radius_with_padding,
            y_center=(col_index + 1) * max_circle_radius_with_padding,
            radius=radius,
        )

plotter.preview()
