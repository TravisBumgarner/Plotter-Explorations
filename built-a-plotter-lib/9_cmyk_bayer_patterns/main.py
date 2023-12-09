from gcode2dplotterart import Plotter2D


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

LAYERS = [CYAN_LAYER, MAGENTA_LAYER, YELLOW_LAYER, BLACK_LAYER]

for layer in LAYERS:
    plotter.add_layer(title=layer, color=layer, line_width=LINE_WIDTH)
