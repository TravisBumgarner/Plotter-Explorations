from gcode2dplotterart import Plotter3D
from gcode2dplotterart import experimental_photo_utils

X_MIN = 0
X_MAX = 170
Y_MIN = 70
Y_MAX = 230
Z_PLOTTING_HEIGHT = 0
Z_NAVIGATION_HEIGHT = 4

MAX_WIDTH = X_MAX - X_MIN
MAX_HEIGHT = Y_MAX - Y_MIN

# Take in an image, such as size 1000x1000. Sample at 5px per, 
# which results in 200x200 grid. Then we can draw 200x200 circles at diameter 1 each.#
SAMPLE_LENGTH = 5
# TBH the math here doesn't quite make sense.
OUTPUT_DIAMETER = SAMPLE_LENGTH / 5

RADIUS_MAPPING = [
    0.9 * OUTPUT_DIAMETER / 2,
    0.7 * OUTPUT_DIAMETER / 2,
    0.5 * OUTPUT_DIAMETER / 2,
    0.3 * OUTPUT_DIAMETER / 2,
    0.1 * OUTPUT_DIAMETER / 2
]

plotter = Plotter3D(
    title="Dogs",
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
        "title": "black_1",
        "color": "#252e2b",
        "line_width": 1,
    },
]

for layer in LAYERS:
    plotter.add_layer(
        layer["title"], color=layer["color"], line_width=layer["line_width"]
    )

image_path = "/Users/travisbumgarner/Documents/gf/3.jpg" 

image = experimental_photo_utils.load_image(image_path)
image = experimental_photo_utils.resize_image(image, MAX_WIDTH * SAMPLE_LENGTH, MAX_HEIGHT * SAMPLE_LENGTH)
# Convert image to float32 before processing to prevent overflow
image = image.astype('float32')
image = experimental_photo_utils.grayscale_image(image, method="average")
image = experimental_photo_utils.buck_image_even_histogram_distribution(
    image, layer_count=len(RADIUS_MAPPING), preview=False
)

def are_all_pixels_in_bounds(row_index, col_index):
    for i in range(int(row_index), int(row_index + SAMPLE_LENGTH)):
        for j in range(int(col_index), int(col_index + SAMPLE_LENGTH)):
            if i < 0 or i >= image.shape[0] or j < 0 or j >= image.shape[1]:
                return False
    return True

def average_area(row_index, col_index):
    if not are_all_pixels_in_bounds(row_index, col_index):
        return -1
    
    total_area = 0
    count = 0
    for i in range(int(row_index), int(row_index + SAMPLE_LENGTH)):
        for j in range(int(col_index), int(col_index + SAMPLE_LENGTH)):
            total_area += image[i, j]
            count += 1
    return int(total_area / count)
print(f"image.shape: {image.shape}")
for row_index in range(0, image.shape[0], SAMPLE_LENGTH):
    # Don't print last row
    if row_index > image.shape[0] - SAMPLE_LENGTH:
        break

    for col_index in range(0, image.shape[1], SAMPLE_LENGTH):
        # Don't print last column
        if col_index > image.shape[1] - SAMPLE_LENGTH:
            break

        radius = RADIUS_MAPPING[average_area(row_index, col_index)]
        if radius == -1:
            continue
        plotter.layers['black_1'].add_circle(
            x_center=X_MIN + col_index / SAMPLE_LENGTH,
            y_center=Y_MIN + row_index / SAMPLE_LENGTH,
            radius=radius)
        
        while radius > 0:
            plotter.layers['black_1'].add_circle(
                x_center=X_MIN + col_index / SAMPLE_LENGTH,
                y_center=Y_MIN + row_index / SAMPLE_LENGTH,
                radius=radius)
            radius -= 1
        
plotter.preview()
plotter.save()
