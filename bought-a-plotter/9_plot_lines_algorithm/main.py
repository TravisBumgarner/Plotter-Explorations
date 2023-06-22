import cv2
import numpy as np
from library import Instructions

def convert_image_to_n_grayscale_colors(img, n = 3):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bucket_segments = 255 / n
    grayscale_buckets = np.rint(np.divide(img, bucket_segments))
    grayscale_buckets.astype(np.uint8)
    return grayscale_buckets


SCALE = 5
OFFSET_X = 100
OFFSET_Y = -50

def main():
    instructions = Instructions()
    img = cv2.imread('test.png')
    grayscale_buckets = convert_image_to_n_grayscale_colors(img)
    print(grayscale_buckets)

    for y, row in enumerate(grayscale_buckets):
        start = [0,y]
        end = None
        value = grayscale_buckets[0][y]
        instructions.add_comment(f'row {y}')

        for x, pixel in enumerate(row):
            if pixel == value:
                continue
            end = [x-1,y]
            instructions.add_line(OFFSET_X + start[0] * SCALE, OFFSET_Y + -1 * start[1] * SCALE, OFFSET_X + end[0] * SCALE, OFFSET_Y + -1 * end[1] * SCALE)
            print(f'value {value} start {start} end {end}')
            start=[x,y]
            value = pixel
        end = [x,y]
        instructions.add_line(OFFSET_X + start[0] * SCALE, OFFSET_Y + -1 * start[1] * SCALE, OFFSET_X + end[0] * SCALE, OFFSET_Y + -1 * end[1] * SCALE)
        print(f'value {value} start {start} end {end}')

    instructions.print_to_file('output.gcode')
main()