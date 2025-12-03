from gcode2dplotterart import Plotter3D, experimental_photo_utils
import random

# Algorithm
# 1. Resize image to MAX_WIDTH / OUTPUT_BOX_SIDE_LENGTH and MAX_HEIGHT / OUTPUT_BOX_SIDE_LENGTH
# 2. Bucket image into numbers OUTPUT_BOX_SIDE_LENGTH * OUTPUT_BOX_SIDE_LENGTH + 1
#     For example, a box of 2x2 can have 0, 1, 2, 3, or 4 cells filled.
# 3. Randomly fill cells per OUTPUT_BOX until == to calculation in step 2.


# Thought - It'd be better if all math was done relative to the origin such that X_MIN and Y_MIn don't need to be added everywhere.
X_MIN = 0
X_MAX = 170
Y_MIN = 70
Y_MAX = 230
Z_PLOTTING_HEIGHT = 0
Z_NAVIGATION_HEIGHT = 4

MAX_WIDTH = X_MAX - X_MIN
MAX_HEIGHT = Y_MAX - Y_MIN


OUTPUT_BOX_SIDE_LENGTH = 2

plotter = Plotter3D(
    title="Unique Boxes",
    x_min=X_MIN,
    x_max=X_MAX,
    y_min=Y_MIN,
    y_max=Y_MAX,
    z_plotting_height=Z_PLOTTING_HEIGHT,
    z_navigation_height=Z_NAVIGATION_HEIGHT,
    feed_rate=10_000,  # Default feed rate
    output_directory="./output",
    handle_out_of_bounds="Warning",  # Warn if points are out of bounds
)

LAYERS = [
    {
        "title": "black",
        "color": "#000000",
        "line_width": 1,
    },
]
COLORS = [layer["title"] for layer in LAYERS]
for layer in LAYERS:
    plotter.add_layer(
        layer["title"], color=layer["color"], line_width=layer["line_width"]
    )

image_path = "./us.jpg"


def get_cells_for_pixel(start_row: int, start_col: int):
    cells = []

    for r in range(start_row, start_row + OUTPUT_BOX_SIDE_LENGTH):
        for c in range(start_col, start_col + OUTPUT_BOX_SIDE_LENGTH):
            cells.append((c, r))
    print("cells", len(cells))
    random.shuffle(cells)
    return cells


def main():
    image = experimental_photo_utils.load_image(image_path)
    image = experimental_photo_utils.resize_image(
        image, int(MAX_WIDTH / 2), int(MAX_HEIGHT / 2)
    )
    # Convert image to float32 before grayscale conversion to prevent overflow, this is probably worth research.
    image = image.astype("float32")
    image = experimental_photo_utils.grayscale_image(image, method="average")
    image = experimental_photo_utils.buck_image_even_histogram_distribution(
        image,
        layer_count=5,
        preview=False,
    )

    for row_index, row in enumerate(image):
        for cell_index, bucket_value in enumerate(row):
            start_col = X_MIN + cell_index * OUTPUT_BOX_SIDE_LENGTH
            start_row = Y_MIN + row_index * OUTPUT_BOX_SIDE_LENGTH

            cells = get_cells_for_pixel(start_row, start_col)
            print("bucket_value", bucket_value, "cells", len(cells))

            # Bad math to invert the colors.
            bucket_value = (
                OUTPUT_BOX_SIDE_LENGTH * OUTPUT_BOX_SIDE_LENGTH - bucket_value
            )

            cells_to_fill = bucket_value
            while cells_to_fill > 0:
                x, y = cells.pop()
                plotter.layers[COLORS[0]].add_point(x, y)
                cells_to_fill -= 1


if __name__ == "__main__":
    main()
    plotter.preview()
    plotter.save()
