import os

from PIL import Image

# User Defined Constants
OUTPUT_WIDTH = 100  # PX
OUTPUT_HEIGHT = 100  # PX
SAMPLE_AREA = (10,10) # w, h of number of pixels that will make one circle
CIRCLE_SIZES = [0, 1, 3, 5]  # PX

# Other Constants
CIRCLE_CENTER = (SAMPLE_AREA[0]/2, SAMPLE_AREA[1]/2)
H_SAMPLES = int(OUTPUT_WIDTH/SAMPLE_AREA[0])  # Number of samples to make horizontally, used for generating output circle grid.
V_SAMPLES = int(OUTPUT_HEIGHT/SAMPLE_AREA[1])  # See previous line
OUTPUT_CIRCLE_GRID = [[0 for col in range(V_SAMPLES)] for row in range(H_SAMPLES)]

def convert_image(img_location):
    with Image.open(img_location) as img:
        INPUT_WIDTH, INPUT_HEIGHT = img.size

        if INPUT_WIDTH > 100 or INPUT_HEIGHT > 100:
            img = img.resize((OUTPUT_WIDTH, OUTPUT_HEIGHT))

        for y in range(0, OUTPUT_HEIGHT):
            for x in range(0, OUTPUT_WIDTH): # Todo figure out proper number of range to not go out of range
                x_min = x * SAMPLE_AREA[0]
                x_max = x * SAMPLE_AREA[0] + SAMPLE_AREA[0]
                y_min = y * SAMPLE_AREA[1]
                y_max = y * SAMPLE_AREA[1] + SAMPLE_AREA[1]

                total = 0
                for i in range(x_min, x_max):
                    for j in range(y_min, y_max):
                        if img.mode == "L": # “L” 8-bit greyscale. 0 means black, 255 means white.
                            pixel_grayscale = img.getpixel((i, j))

                        else:
                            pixel_rgb_sum = 0
                            for each_pixel in img.getpixel((i, j)):
                                pixel_rgb_sum += each_pixel
                            pixel_grayscale = pixel_rgb_sum  / 3
                        total += pixel_grayscale
                average = round(total / ((x_max - x_min) * (y_max - y_min)))
                print(average)
                OUTPUT_CIRCLE_GRID[y][x] = average

        pixels_out = []
        image_out = Image.new("L", (H_SAMPLES, V_SAMPLES)) # “L” 8-bit greyscale. 0 means black, 255 means white.
        for row in OUTPUT_CIRCLE_GRID:
            for cell in row:
                pixels_out.append(cell)
        image_out.putdata(pixels_out)
        image_out.save('test_out3.png')






        filepath, filename = os.path.split(img_location)
        name, extension = filename.split('.')
        output_location = os.path.join(filepath, name + '_output2.' + extension)
        img.save(output_location)


if __name__ == '__main__':
    convert_image('./test.jpg')