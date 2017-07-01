# README
# Start with Square Images Only


import os

from PIL import Image

# User Defined Constants
OUTPUT_LENGTH = 200  # PX
SAMPLE_LENGTH = 5

CIRCLE_SIZES = [0, 1, 3, 5]  # PX

# Other Constants
CIRCLE_CENTER = (SAMPLE_LENGTH/2, SAMPLE_LENGTH/2)
NUMBER_OF_SAMPLES = int(OUTPUT_LENGTH/SAMPLE_LENGTH)  # Number of samples to make in one direction, used for generating output circle grid.
OUTPUT_CIRCLE_GRID = [[0 for col in range(NUMBER_OF_SAMPLES)] for row in range(NUMBER_OF_SAMPLES)]

def sample_area(img, x_start, y_start, length):
    total = 0
    for y in range(y_start, y_start + length):
        for x in range(x_start, x_start + length):
            if img.mode == "L":  # “L” 8-bit greyscale. 0 means black, 255 means white.
                pixel_grayscale = img.getpixel((x, y))
            else:
                pixel_rgb_sum = 0
                for each_pixel in img.getpixel((x, y)): # take average of R, G, B
                    pixel_rgb_sum += each_pixel
                pixel_grayscale = pixel_rgb_sum / 3
            total += pixel_grayscale
    average = round(total / length ** 2)
    return average


def convert_image(img_location):
    with Image.open(img_location) as img:
        INPUT_LENGTH, _ = img.size

        # Resize Image if one side is > OUTPUT_LENGTH
        if INPUT_LENGTH > OUTPUT_LENGTH:
            img = img.resize((OUTPUT_LENGTH, OUTPUT_LENGTH))

        x_idx = 0
        for x in range(0, OUTPUT_LENGTH, SAMPLE_LENGTH):
            y_idx = 0
            for y in range(0, OUTPUT_LENGTH, SAMPLE_LENGTH):
                OUTPUT_CIRCLE_GRID[y_idx][x_idx] = sample_area(img, x, y, SAMPLE_LENGTH)
                y_idx += 1
            x_idx += 1


        pixels_out = []
        image_out = Image.new("L", (NUMBER_OF_SAMPLES, NUMBER_OF_SAMPLES)) # “L” 8-bit greyscale. 0 means black, 255 means white.
        for row in OUTPUT_CIRCLE_GRID:
            for cell in row:
                pixels_out.append(cell)
        image_out.putdata(pixels_out)
        image_out.save('test_out4.png')

        filepath, filename = os.path.split(img_location)
        name, extension = filename.split('.')
        output_location = os.path.join(filepath, name + '_output2.' + extension)
        img.save(output_location)


if __name__ == '__main__':
    convert_image('./test2.jpg')