from gcode2dplotterart import Plotter3D
from gcode2dplotterart import experimental_photo_utils
import random
import math

X_MIN = 0
X_MAX = 170
Y_MIN = 70
Y_MAX = 230
Z_PLOTTING_HEIGHT = 0
Z_NAVIGATION_HEIGHT = 4

MAX_WIDTH = X_MAX - X_MIN
MAX_HEIGHT = Y_MAX - Y_MIN

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
        "title": "cyan",
        "color": "#00ffff",
        "line_width": 1,
    },
    {
        "title": "magenta",
        "color": "#ff00ff",
        "line_width": 1,
    },
    {
        "title": "yellow",
        "color": "#ffff00",
        "line_width": 1,
    },
    {
        "title": "black",
        "color": "#000000",
        "line_width": 1,
    },
]
COLORS = [layer['title'] for layer in LAYERS]

for layer in LAYERS:
    plotter.add_layer(
        layer["title"], color=layer["color"], line_width=layer["line_width"]
    )

def draw_box(x, y, width, height, color1, color2, color3, color4):
    plotter.layers[color1].add_line(X_MIN + x, Y_MIN + y, X_MIN + x + width, Y_MIN + y,)
    plotter.layers[color2].add_line(X_MIN + x + width, Y_MIN + y, X_MIN + x + width, Y_MIN + y + height,)
    plotter.layers[color3].add_line(X_MIN + x + width, Y_MIN + y + height, X_MIN + x, Y_MIN + y + height,)
    plotter.layers[color4].add_line(X_MIN + x, Y_MIN + y + height, X_MIN + x, Y_MIN + y,)


def generate_colors():
    return [
        random.choice(COLORS) for _ in range(0,3)
    ]

SIDE_LENGTH = 7

def generate_all_color_combinations():
    """Generate all possible unique combinations of 4 colors for a square's sides"""
    all_combinations = []
    for c1 in COLORS:
        for c2 in COLORS:
            for c3 in COLORS:
                for c4 in COLORS:
                    all_combinations.append((c1, c2, c3, c4))
    random.shuffle(all_combinations)
    return all_combinations

def main():
    # Get all possible color combinations
    all_combinations = generate_all_color_combinations()
    print(len(all_combinations))
    
    # Calculate grid layout
    box_count = len(all_combinations)  # Will be 256 (4^4)
    grid_size = math.ceil(math.sqrt(box_count))
    
    # Calculate box spacing to fit all boxes
    spacing = SIDE_LENGTH + 3  # Add 5 units of padding between boxes
    
    for idx, colors in enumerate(all_combinations):
        # Calculate grid position
        row = idx // grid_size
        col = idx % grid_size
        
        # Calculate box position
        x = col * spacing
        y = row * spacing
        
        # Draw box with current color combination
        draw_box(x, y, SIDE_LENGTH, SIDE_LENGTH, *colors)

if __name__ == "__main__":
    main()

plotter.preview()
plotter.save()
