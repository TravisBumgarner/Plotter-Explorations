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

        if (self.input_width / self.output_width - self.input_height / self.output_height) > 0.1:
            print('[!] The ratio of size from input image to output image is quite different. Consider editing first')

        if SPACING_BETWEEN_CIRCLE_CENTERS < MAX_DIAMETER:
            print('[!] The SPACING_BETWEEN_CIRCLE_CENTERS should be greater than the MAX_DIAMETER')

        x_circles = int(self.output_width / self.output_spacing)
        y_circles = int(self.output_height / self.output_spacing)
        total_circles = int(x_circles * y_circles)
        response = raw_input('X Circles: {}\nY Circles: {}\nTotal Circles: {}\nContinue? [y/n]'.format(x_circles, y_circles, total_circles))
        if response != 'y' or 'Y':
            return

    def luminance_to_circle_radius(self, value):
        mod_value = (255 - value) if WHITE_MEANS_SMALL_CIRCLES else value
        diameter = self.output_min_diameter + (float(mod_value) / float(255) * (self.output_max_diameter - self.output_min_diameter))
        radius = diameter / 2
        return radius

    def sample_image(self):
        print('Sampling Image...')
        self.sample_data = []

        total_x_samples = self.output_width / self.output_spacing
        total_y_samples = self.output_height / self.output_spacing

        pixels_per_sample_width = int(round(self.input_width / total_x_samples))
        pixels_per_sample_height = int(round(self.input_height / total_y_samples))

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
        self.sample_data.reverse() # dxf has (+x,+y) in 1, while the image is sampled differently so this corrects it for dxf.
        print('Sampling Complete.')

    def sample_image_area(self, x_start, x_delta, y_start, y_delta):
        luminance_total = 0
        for x in range(x_start, x_start + x_delta):
            for y in range(y_start, y_start + y_delta):
                luminance_total += self.img.getpixel((x, y))

        sample_area = x_delta * y_delta
        luminance_average = luminance_total / sample_area
        return luminance_average

    def samples_to_dxf(self):
        print('Converting samples to dxf...')
        x_center = 0
        y_center = 0

        for row in self.sample_data:
            for sample_luminance_value in row:
                circle = dxf.circle(radius=self.luminance_to_circle_radius(sample_luminance_value))
                self.dxf_drawing.add(circle, center=(x_center, y_center))
                x_center += self.output_spacing
            x_center = 0
            y_center += self.output_spacing
        print('Converting Complete.')

    def draw_borders(self):
        min_x = -self.output_spacing
        max_x = self.output_width
        min_y = -self.output_spacing
        max_y = self.output_height

        self.dxf_drawing.add(dxf.line(start=(min_x, min_y), end=(min_x, max_y)))
        self.dxf_drawing.add(dxf.line(start=(min_x, min_y), end=(max_x, min_y)))
        self.dxf_drawing.add(dxf.line(start=(max_x, min_y), end=(max_x, max_y)))
        self.dxf_drawing.add(dxf.line(start=(min_x, max_y), end=(max_x, max_y)))

    def save_dxf(self):
        self.dxf_drawing.save()
        print('Saving as {}'.format(DXF_FILE))


if __name__ == '__main__':
    r = RasterImage(IMAGE_FILE)
    r.sample_image()
    r.samples_to_dxf()
    r.draw_borders()
    r.save_dxf()

