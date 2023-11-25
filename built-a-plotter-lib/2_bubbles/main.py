from gcode2dplotterart import Plotter2D
from random import randrange, choice, randint

LINE_WIDTH = 1.0

COLORS = [
    {"title": "purple1", "color": "#EABEFF"},
    {"title": "blue1", "color": "#A2FFF8"},
    {"title": "orange1", "color": "#FF7700"},
    {"title": "purple2", "color": "#AD00FF"},
    {"title": "grey1", "color": "#E9E9E9"},
]

# Create a plotter object
plotter = Plotter2D(
    title="Circles",
    x_min=0,
    x_max=260,
    y_min=0,
    y_max=200,
    feed_rate=10000,
)

for color in COLORS:
    plotter.add_layer(
        title=color["title"],
        color=color["color"],
        line_width=LINE_WIDTH,
    )

print
counter = 0
STARTING_CIRCLES = 500

while counter < STARTING_CIRCLES:
    x_center = randrange(int(plotter.x_min), int(plotter.x_max))
    y_center = randrange(int(plotter.y_min), int(plotter.y_max))

    min_distance_to_edge = min(
        abs(x_center - plotter.x_min),
        abs(plotter.x_max - x_center),
        abs(y_center - plotter.y_min),
        abs(plotter.y_max - y_center),
    )

    remaining_radius = min(randint(0, 20), min_distance_to_edge)

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