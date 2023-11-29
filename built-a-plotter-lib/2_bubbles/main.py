from gcode2dplotterart import Plotter2D
from random import randrange, choice, randint

LINE_WIDTH = 1.0

COLORS = [
    {"title": "4_green1", "color": "#A9FF00"},
    {"title": "6_blue1", "color": "#A2FFF8"},
    {"title": "7_blue2", "color": "#0024FF"},
    {"title": "c_purple2", "color": "#AD00FF"},
    {"title": "a_pink2", "color": "#FF0096"},
    {"title": "f_grey3", "color": "#1E1E1E"},
]

# Create a plotter object
plotter = Plotter2D(
    title="Bubbles",
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
STARTING_CIRCLES = 100

center_points = []


def is_near_existing_center_point(x, y):
    for center_point in center_points:
        if abs(center_point[0] - x) < 15 and abs(center_point[1] - y) < 15:
            return True
    return False


while counter < STARTING_CIRCLES:
    attempt_to_find_better_center = 0

    while attempt_to_find_better_center < 100000:
        x_center = randrange(int(plotter.x_min), int(plotter.x_max))
        y_center = randrange(int(plotter.y_min), int(plotter.y_max))

        if not is_near_existing_center_point(x_center, y_center):
            break
        attempt_to_find_better_center += 1
    print("attempt_to_find_better_center", attempt_to_find_better_center)

    center_points.append([x_center, y_center])
    x_center = randrange(int(plotter.x_min), int(plotter.x_max))
    y_center = randrange(int(plotter.y_min), int(plotter.y_max))

    min_distance_to_edge = min(
        abs(x_center - plotter.x_min),
        abs(plotter.x_max - x_center),
        abs(y_center - plotter.y_min),
        abs(plotter.y_max - y_center),
    )

    remaining_radius = min(randint(0, 10), min_distance_to_edge)

    first_circle = True
    while remaining_radius > 0:
        layer = "f_grey3" if first_circle else choice(COLORS)["title"]
        plotter.layers[layer].add_circle(
            x_center,
            y_center,
            radius=remaining_radius,
        )
        remaining_radius -= randint(int(LINE_WIDTH), int(LINE_WIDTH * 5))
        first_circle = False
    counter += 1


plotter.preview()

plotter.save()
