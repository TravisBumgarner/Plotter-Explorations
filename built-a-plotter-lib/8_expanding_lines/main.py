from gcode2dplotterart import Plotter2D
import math
from random import randint

LINE_WIDTH = 0.5
LAYER_0 = {"title": "black", "color": "black", "line_width": LINE_WIDTH}

layers = [
    LAYER_0,
]

plotter = Plotter2D(
    title="Expanding Shapes",
    x_min=0,
    x_max=180,
    y_min=0,
    y_max=180,
    feed_rate=10000,
    include_comments=False,
)

for layer in layers:
    plotter.add_layer(**layer)


def is_point_in_circle(x, y, x_center, y_center, radius):
    distance = math.sqrt((x - x_center) ** 2 + (y - y_center) ** 2)
    return distance <= radius


def closest_point_on_circle_edge(x, y, x_center, y_center, radius):
    vector_x = x - x_center
    vector_y = y - y_center

    distance = math.sqrt(vector_x**2 + vector_y**2)

    normalized_vector_x = vector_x / distance
    normalized_vector_y = vector_y / distance

    closest_x = x_center + normalized_vector_x * radius
    closest_y = y_center + normalized_vector_y * radius

    return closest_x, closest_y


def point_along_line(x1, y1, x2, y2, hypotenuse):
    print(x1, y1, x2, y2)
    vector_x = x2 - x1
    vector_y = y2 - y1

    distance = math.sqrt(vector_x**2 + vector_y**2)

    normalized_vector_x = vector_x / distance
    normalized_vector_y = vector_y / distance

    scaled_vector_x = normalized_vector_x * hypotenuse
    scaled_vector_y = normalized_vector_y * hypotenuse

    x3 = x1 + scaled_vector_x
    y3 = y1 + scaled_vector_y

    return x3, y3


def midpoint_if_far(x1, y1, x2, y2, hypotenuse):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    if distance > hypotenuse:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        return mid_x, mid_y
    else:
        return None


x_center = (plotter.x_max - plotter.x_min) / 2
y_center = (plotter.y_max - plotter.y_min) / 2
radius = plotter.width / 2

num_points = 11

# Generate the points on the circle using parametric equations
current_path = []
for i in range(num_points):
    angle = 2 * math.pi * i / num_points
    x = x_center + 3 * math.cos(angle)
    y = y_center + 3 * math.sin(angle)
    current_path.append((x, y))
current_path.append(current_path[0])


print(current_path)


def add_line_breaks(path, hypotenuse):
    new_path = []
    for i in range(len(path) - 1):
        point_a = path[i]
        point_b = path[i + 1]
        mid_point = midpoint_if_far(
            point_a[0], point_a[1], point_b[0], point_b[1], hypotenuse
        )
        if mid_point:
            new_path.append(point_a)
            new_path.append(mid_point)
        else:
            new_path.append(point_a)
    new_path.append(path[-1])
    return new_path


def expand_path_outwards(path: list) -> [list, bool]:
    some_points_inside_circle = False
    next_path = []

    for point in current_path[0:-1]:
        point_to_move_towards = closest_point_on_circle_edge(
            point[0], point[1], x_center, y_center, radius
        )

        if point == point_to_move_towards:
            next_path.append(point)
            continue

        next_point = point_along_line(
            point[0],
            point[1],
            point_to_move_towards[0],
            point_to_move_towards[1],
            hypotenuse=1,
        )

        if is_point_in_circle(next_point[0], next_point[1], x_center, y_center, radius):
            some_points_inside_circle = True
            next_path.append(next_point)
            point = next_point
        else:
            next_path.append(point)
    # Append the starting point to complete the shape.
    next_path.append(current_path[0])
    return [next_path, some_points_inside_circle]


some_points_inside_circle = True
while some_points_inside_circle:
    some_points_inside_circle = False
    plotter.layers[LAYER_0["title"]].add_path(current_path)

    current_path = add_line_breaks(current_path, hypotenuse=10)

    [next_path, some_points_inside_circle] = expand_path_outwards(current_path)

    current_path = next_path

plotter.preview()
plotter.save()
