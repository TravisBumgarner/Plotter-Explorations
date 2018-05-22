from PIL import Image
from dxfwrite import DXFEngine as dxf

# https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another



class RasterImage():
    """"
    Description: Foo
    """

    def __init__(self, img_src):
        """Creates a new RasterImage"""
        try:
            self.img = Image.open(img_src).convert('L') # Convert to grayscale
        except IOError:
            print('[-] Not a valid image')
            return

        self.input_width, self.input_height = self.img.size
        #
        # self.output_units = ''
        # while self.output_units not in ['in', 'cm']:
        #     self.output_units = raw_input('[>] Select project units(in or cm): ')
        #
        # self.output_width = float(raw_input('[>] Output width: '))
        # self.output_height = float(raw_input('[>] Output height: '))
        #
        # if(self.input_width / self.output_width - self.input_height / self.output_height > 0.1):
        #     print('[!] The ratio of size from input image to output image is quite different. Consider editing first')
        #
        # self.output_spacing = float(raw_input('[>] Output density (circles per {}: ').format(self.output_units))
        # spacing = float(raw_input('[>] Spacing between circles:'))
        # self.output_max_diameter = 1 / self.output_spacing - spacing / 2
        #
        self.output_units = 'in'
        self.output_width = 4
        self.output_height = 4
        self.output_spacing = 0.15
        self.output_max_diameter = self.output_spacing * 0.9 # max diameter should be slightly smaller than spacing between circles
        self.output_min_diameter = 0.002 # 1/32"
        self.sample_data = []

        self.dxf_drawing = dxf.drawing('/Users/tbumgarner/Documents/Programming/raster_cutter/foo.dxf')

    def luminance_to_inches(self, value):
        # 255 - value inverts the value so that the largest circles are for the darkest places.
        if value == 255:
            # Don't print circles for values of 255.
            inches = 0
        else:
            inches = self.output_min_diameter + (float(255 - value) / float(255) * (self.output_max_diameter - self.output_min_diameter))
        return inches

    def sample_image(self):
        self.sample_data = []

        width_samples = self.output_width / self.output_spacing
        height_samples = self.output_height / self.output_spacing

        pixels_per_sample_width = int(round(self.input_width / width_samples))
        pixels_per_sample_height = int(round(self.input_height / height_samples))

        x = 0
        y = 0

        # Swap x and y
        # while x + pixels_per_sample_width <= self.input_width:
        while y + pixels_per_sample_height <= self.input_height:
            sample_row_data = []
            # while y + pixels_per_sample_height <= self.input_height:
            while x + pixels_per_sample_width <= self.input_width:
                luminance = self.sample_image_area(x, pixels_per_sample_width, y, pixels_per_sample_height)
                sample_row_data.append(luminance)
                # y += pixels_per_sample_height
                x += pixels_per_sample_width
            # y = 0
            x = 0
            self.sample_data.append(sample_row_data)
            # x += pixels_per_sample_width
            y += pixels_per_sample_height

    def samples_to_dxf(self):
        x = 0
        y = 0

        for row in self.sample_data:
            for cell in row:
                self.dxf_drawing.add(dxf.circle(radius=self.luminance_to_inches(cell) / 2, center=(x, y)))
                y += self.output_spacing
            y = 0
            x += self.output_spacing

    def sample_image_area(self, x_start, x_delta, y_start, y_delta):
        luminance_total = 0
        for x in range(x_start, x_start + x_delta):
            for y in range(y_start, y_start + y_delta):
                luminance_total += self.img.getpixel((x, y))

        sample_area = x_delta * y_delta
        luminance_average = luminance_total / sample_area
        # print("sampling - ({}, {}) -> {}".format(x_start, y_start, luminance_average))
        return luminance_average

    def draw_borders(self):
        min_x = 0 - self.output_spacing
        max_x = self.output_width - self.output_spacing
        min_y = 0 - self.output_spacing
        max_y = self.output_height - self.output_spacing

        self.dxf_drawing.add(dxf.line(start=(min_x, min_y), end=(min_x, max_y)))
        self.dxf_drawing.add(dxf.line(start=(min_x, min_y), end=(max_x, min_y)))
        self.dxf_drawing.add(dxf.line(start=(max_x, min_y), end=(max_x, max_y)))
        self.dxf_drawing.add(dxf.line(start=(min_x, max_y), end=(max_x, max_y)))

    def save_dxf(self):
        self.dxf_drawing.save()

if __name__ == '__main__':
    r = RasterImage('./src/chs.jpg')
    r.sample_image()
    print('image sampled')
    r.samples_to_dxf()
    r.draw_borders()
    r.save_dxf()

