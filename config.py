# Currently the only thing that matters here are the ratios between values. Can't find inches in the dxf library
UNITS = 'in'
WIDTH_OVER_HEIGHT_RATIO = 0.737
HEIGHT = 4
WIDTH = HEIGHT * WIDTH_OVER_HEIGHT_RATIO
SPACING_BETWEEN_CIRCLE_CENTERS = 0.08
MAX_DIAMETER = SPACING_BETWEEN_CIRCLE_CENTERS * 0.75
MIN_DIAMETER = 0.002
SAMPLE_DATA = []
IMAGE_FILE = './src/dog2.jpg'
DXF_FILE = './output/chs.dxf'
BLACK_MEANS_SMALL_CIRCLES = False
