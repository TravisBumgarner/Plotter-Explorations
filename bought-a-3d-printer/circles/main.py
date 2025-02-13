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

MAX_RADIUS = 2.5
MAX_DIAMETER = int(2 * MAX_RADIUS)

RADIUS_MAPPING = [
    0.2 * MAX_RADIUS,
    0.4 * MAX_RADIUS,
    0.6 * MAX_RADIUS,
    0.8 * MAX_RADIUS,
    1 * MAX_RADIUS
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

image_path = "/Users/travisbumgarner/Documents/gf/2.jpg" 

image = experimental_photo_utils.load_image(image_path)
image = experimental_photo_utils.resize_image(image, MAX_WIDTH * MAX_DIAMETER, MAX_HEIGHT * MAX_DIAMETER)
# Convert image to float32 before processing to prevent overflow
image = image.astype('float32')
image = experimental_photo_utils.grayscale_image(image, method="average")
image = experimental_photo_utils.buck_image_even_histogram_distribution(
    image, layer_count=len(RADIUS_MAPPING), preview=False
)

def are_all_pixels_in_bounds(row_index, col_index):
    for i in range(int(row_index), int(row_index + MAX_DIAMETER)):
        for j in range(int(col_index), int(col_index + MAX_DIAMETER)):
            if i < 0 or i >= image.shape[0] or j < 0 or j >= image.shape[1]:
                return False
    return True

def average_area(row_index, col_index):
    if not are_all_pixels_in_bounds(row_index, col_index):
        return -1
    
    total_area = 0
    count = 0
    for i in range(int(row_index), int(row_index + MAX_DIAMETER)):
        for j in range(int(col_index), int(col_index + MAX_DIAMETER)):
            total_area += image[i, j]
            count += 1
    return int(total_area / count)
print(f"image.shape: {image.shape}")
for row_index in range(0, image.shape[0], MAX_DIAMETER):
    # Don't print last row
    if row_index > image.shape[0] - MAX_DIAMETER:
        break

    for col_index in range(0, image.shape[1], MAX_DIAMETER):
        # Don't print last column
        if col_index > image.shape[1] - MAX_DIAMETER:
            break

        radius = RADIUS_MAPPING[average_area(row_index, col_index)]
        if radius == -1:
            continue
        plotter.layers['black_1'].add_circle(
            x_center=X_MIN + col_index / MAX_DIAMETER + MAX_DIAMETER,
            y_center=Y_MIN + row_index / MAX_DIAMETER + MAX_DIAMETER,
            radius=radius)
        
plotter.preview()
plotter.save()
