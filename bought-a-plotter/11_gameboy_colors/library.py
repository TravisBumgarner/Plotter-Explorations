from enum import Enum
import matplotlib.pyplot as plt
from PIL import Image

class Point:
    def __init__(self, feed_rate: float, x: float | None = None, y: float | None = None):
        self.x = x
        self.y = y
        self.feed_rate = feed_rate

        if(x is None and y is None):
            raise ValueError("Point requires an X or Y")

    def __str__(self):
        output = "G1 "
        if(self.x is not None):
            output += f"X{self.x:.3f} "
        if(self.y is not None):
            output += f"Y{self.y:.3f} "
        output += f"F{self.feed_rate}"
        return output


class SpecialInstruction(Enum):
    PEN_UP = "M3 S0"
    PAUSE = "G04 P0.25" # Might need to refine this number
    PEN_DOWN = "M3 S1000"
    PROGRAM_END = "M2"


def preview_gcode(filename: str, output_image: str):
    is_plotting = None
    x_coords = []
    y_coords = []

    with open(filename, 'r') as file:
        instructions = file.readlines()
    
    for instruction in instructions:
        if instruction.startswith('G1'):
            elements = instruction.split()
            for element in elements:
                if element.startswith('X'):
                    x_coords.append(float(element[1:]))
                elif element.startswith('Y'):
                    y_coords.append(float(element[1:]))
        elif instruction.startswith('M3'):
            elements = instruction.split()
            if element.startswith('S'):
                value = float(element[1:])
                if value == 0:
                    is_plotting = False
                elif value == 1000:
                    is_plotting = True
           

class Instructions:
    def __init__(self, units = 'mm', feed_rate = 10000.0, x_min = 0, x_max = 260.0, y_min = -180, y_max = 0):
        self.feed_rate = feed_rate
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.setup = []
        self.instructions = []
        self.teardown = []
        self.has_plotted_first_point = False

        if units == 'mm':
            self.setup.append('G21')
        if units == 'inches':
            self.setup.append('G20')

        self.setup.append(f"F{self.feed_rate}")

        self.teardown.append(SpecialInstruction.PROGRAM_END.value)

    def add_plotting_outline(self, number_of_outlines=3):
        # Todo - Should only execute once it knows how big the plotting area is
        self.add_comment('Plotting area outline')
        for _ in range(number_of_outlines):
            self.add_special(SpecialInstruction.PEN_UP, 'setup')
            self.add_point(self.x_max, self.y_min, 'setup')
            self.add_point(self.x_max, self.y_max, 'setup')
            self.add_point(self.x_min, self.y_max, 'setup')
            self.add_point(self.x_min, self.y_min, 'setup')
            self.add_point(self.x_max, self.y_min, 'setup')

    def add_first_point(self, x, y):
        self.add_special(SpecialInstruction.PEN_UP)
        self.add_special(SpecialInstruction.PAUSE)
        self.add_point(x, y)
        self.add_special(SpecialInstruction.PEN_DOWN)
        self.add_special(SpecialInstruction.PAUSE)

    def add_line(self, x1, y1, x2, y2):
        self.add_first_point(x1, y1)
        self.add_point(x2, y2)

    def add_point(self, x, y, type="instructions"):
        point = Point(self.feed_rate, x, y)
        
        if not self.is_point_valid(point):
            raise ValueError("Failed to add point, outside dimensions of plotter", point.x, point.y)
        
        if type == "instructions":
            self.instructions.append(point)
        elif type == "setup":
            self.setup.append(point)
        elif type == "teardown":
            self.teardown.append(point)
        
    def add_special(self, special_instruction: SpecialInstruction, type="instructions"):
        if type == "instructions":
            self.instructions.append(special_instruction.value)
        elif type == "setup":
            self.setup.append(special_instruction.value)
        elif type == "teardown":
            self.teardown.append(special_instruction.value)
            
    def is_point_valid(self, point: Point):
        if point.x > self.x_max or point.y > self.y_max or point.x < self.x_min or point.y < self.y_min:
            return False
        else:
            return True
        
    def print_to_file(self, filename: str):
        with open(filename, "w") as file:
            file.write("\n".join([str(instruction) for instruction in self.setup]))
            file.write("\n")
            file.write("\n".join([str(instruction) for instruction in self.instructions]))
            file.write("\n")
            file.write("\n".join([str(instruction) for instruction in self.teardown]))

    def add_comment(self, comment: str):
        self.instructions.append(f"\n\n; {comment}\n\n")

    def bulk_add(self, instructions):
        self.instructions += instructions.get()

    def get(self):
        return self.instructions
 