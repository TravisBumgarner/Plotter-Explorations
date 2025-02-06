from gcode2dplotterart import Plotter3D
from random import randrange, choice, randint

LINE_WIDTH = 1.0
## RGB
COLORS = [
    {
        "title": "blue",
        "color": "#0000FF",
        "line_width": 1.0,
    },
    {
        "title": "green",
        "color": "#00FF00",
        "line_width": 1.0,
    },
    {
        "title": "red",
        "color": "#FF0000",
        "line_width": 1.0,
    },
]

# Create a plotter object
# X_MIN = 0
# X_MAX = 180
# Y_MIN = 70
# Y_MAX = 230
X_MIN = 0
X_MAX = 50
Y_MIN = 100
Y_MAX = 150
Z_PLOTTING_HEIGHT = 0
Z_NAVIGATION_HEIGHT = 4

# Initialize the plotter
plotter = Plotter3D(
    title="Polygones Réguliers - Dessin 32",
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

for color in COLORS:
    plotter.add_layer(
        title=color["title"],
        color=color["color"],
        line_width=LINE_WIDTH,
    )


counter = 0
STARTING_CIRCLES = 200

while counter < STARTING_CIRCLES:
    x_center = randrange(int(plotter.x_min), int(plotter.x_max))
    y_center = randrange(int(plotter.y_min), int(plotter.y_max))

    min_distance_to_edge = min(
        abs(x_center - plotter.x_min),
        abs(plotter.x_max - x_center),
        abs(y_center - plotter.y_min),
        abs(plotter.y_max - y_center),
    )

    remaining_radius = min(randint(0, 8), min_distance_to_edge)

    while remaining_radius > 0:
        color = choice(COLORS)
        layer = color["title"]
        plotter.layers[layer].add_circle(
            x_center,
            y_center,
            radius=remaining_radius,
        )
        remaining_radius -= randint(int(LINE_WIDTH), int(remaining_radius))
    counter += 1


plotter.preview()

plotter.save()
