from PIL import Image
from dxfwrite import DXFEngine as dxf

from config import *


class RasterImage():
    def __init__(self, img_src):
        try:
            self.img = Image.open(img_src).convert('L') # Convert to grayscale
        except IOError:
            print('[-] Not a valid image')
            return

        self.input_width, self.input_height = self.img.size

        # Currently the only thing that matters here are the ratios between values. Can't find inches in the dxf library
        self.output_units = UNITS
        self.output_width = WIDTH
        self.output_height = HEIGHT
        self.output_spacing = SPACING_BETWEEN_CIRCLE_CENTERS
        self.output_max_diameter = MAX_DIAMETER
        self.output_min_diameter = MIN_DIAMETER
        self.sample_data = []
        self.dxf_drawing = dxf.drawing(DXF_FILE)

        if self.input_width / self.output_width - self.input_height / self.output_height > 0.1:
            print('[!] The ratio of size from input image to output image is quite different. Consider editing first')

        if SPACING_BETWEEN_CIRCLE_CENTERS < MAX_DIAMETER:
            print('[!] The SPACING_BETWEEN_CIRCLE_CENTERS should be greater than the MAX_DIAMETER')

        x_circles = int(self.output_width / self.output_spacing)
        y_circles = int(self.output_height / self.output_spacing)
        total_circles = int(x_circles * y_circles)
        response = raw_input('X Circles: {}\nY Circles: {}\nTotal Circles: {}\nContinue? [y/n]'.format(x_circles, y_circles, total_circles))
        if response != 'y' or 'Y':
            return

    def luminance_to_inches(self, value):
        # 255 - value inverts the value so that the largest circles are for the darkest places.
        if value == 255:
            # Don't print circles for values of 255.
            inches = 0
        else:
            inches = self.output_min_diameter + (float(255 - value) / float(255) * (self.output_max_diameter - self.output_min_diameter))
        return inches

    def sample_image(self):
        print('Sampling Image...')
        self.sample_data = []

        width_samples = self.output_width / self.output_spacing
        height_samples = self.output_height / self.output_spacing

        pixels_per_sample_width = int(round(self.input_width / width_samples))
        pixels_per_sample_height = int(round(self.input_height / height_samples))

        x = 0
        y = 0

        while y + pixels_per_sample_height <= self.input_height:
            sample_row_data = []
            while x + pixels_per_sample_width <= self.input_width:
                luminance = self.sample_image_area(x, pixels_per_sample_width, y, pixels_per_sample_height)
                sample_row_data.append(luminance)
                x += pixels_per_sample_width
            x = 0
            self.sample_data.append(sample_row_data)
            y += pixels_per_sample_height
        print('Sampling Complete.')

    def samples_to_dxf(self):
        print('Converting samples to dxf...')
        # Start at the center of the first square
        x = self.output_spacing / 2
        y = self.output_spacing / 2

        for row in self.sample_data:
            for cell in row:
                self.dxf_drawing.add(dxf.circle(radius=self.luminance_to_inches(cell) / 2, center=(x, y)))
                y += self.output_spacing
            y = self.output_spacing / 2
            x += self.output_spacing
        print('Converting Complete.')

    def sample_image_area(self, x_start, x_delta, y_start, y_delta):
        luminance_total = 0
        for x in range(x_start, x_start + x_delta):
            for y in range(y_start, y_start + y_delta):
                luminance_total += self.img.getpixel((x, y))

        sample_area = x_delta * y_delta
        luminance_average = luminance_total / sample_area
        return luminance_average

    def draw_borders(self):
        min_x = 0
        max_x = self.output_width - self.output_spacing / 2
        min_y = 0
        max_y = self.output_height - self.output_spacing / 2

        self.dxf_drawing.add(dxf.line(start=(min_x, min_y), end=(min_x, max_y)))
        self.dxf_drawing.add(dxf.line(start=(min_x, min_y), end=(max_x, min_y)))
        self.dxf_drawing.add(dxf.line(start=(max_x, min_y), end=(max_x, max_y)))
        self.dxf_drawing.add(dxf.line(start=(min_x, max_y), end=(max_x, max_y)))

    def save_dxf(self):
        self.dxf_drawing.save()


if __name__ == '__main__':
    r = RasterImage(IMAGE_FILE)
    r.sample_image()
    r.samples_to_dxf()
    r.draw_borders()
    r.save_dxf()

