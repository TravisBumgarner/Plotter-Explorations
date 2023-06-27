import cv2
import numpy as np
from library import Instructions
from imutils import resize

SCALE = 3

# I could probably not have me hit the bounds of the plotter with some better math.
# Oh well. For now, this mess.
magic_number = 10
hmmm = Instructions()
IMG_RESIZE_X = int(hmmm.x_max / SCALE) - magic_number
IMG_RESIZE_Y = int(abs(hmmm.y_max / SCALE)) - magic_number

# Still need to do something with this function
def most_interesting_colors(img, n_colors):
    pixels = np.float32(img.reshape(-1, 3))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    for [b,g,r] in palette:
        r = hex(int(r)).replace("0x", "").rjust(2, '0')
        b = hex(int(b)).replace("0x", "").rjust(2, '0')
        g = hex(int(g)).replace("0x", "").rjust(2, '0')

        print(f'#{r}{g}{b}')

    # return np.uint8(palette[-1])


def convert_image_to_n_grayscale_colors(filename, n):
    img = cv2.imread(filename)
    most_interesting_colors(img, n)
    img = resize(img, width=IMG_RESIZE_X, height=IMG_RESIZE_Y)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bucket_segments = 255 / (n - 1)
    grayscale_buckets = np.rint(np.divide(img, bucket_segments))
    grayscale_buckets.astype(np.uint8)
    print('outputting array', grayscale_buckets.shape)
    return grayscale_buckets



OFFSET_X = 0
OFFSET_Y = 0

BUCKETS = 4

# based on assumptions of outputs being darkest to lightest. 
labels = {
    0: 'grey',
    1: 'blue',
    2: 'yellow',
    3: 'orange',
}


def main():
    filename="test7.png"
    instructionSets = [Instructions() for _ in range(BUCKETS)]
    instructionSets[0].add_plotting_outline(2)
    # Works with color PNGs exported from lightroom
    grayscale_buckets = convert_image_to_n_grayscale_colors(filename,  BUCKETS)

   
main()