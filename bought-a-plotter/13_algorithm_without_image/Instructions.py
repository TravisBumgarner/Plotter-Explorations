from enum import Enum

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


class Instructions:
    def __init__(self, units, x_min, x_max, y_min, y_max, feed_rate, should_outline=False):
        self.units = units
        if units not in ['mm', 'inches']:
            raise ValueError("Units must be mm or inches")  
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.feed_rate = feed_rate

        self.setup_instructions = []
        self.plotting_instructions = []
        self.teardown_instructions = []
        self.has_plotted_first_point = False
        self.should_outline = should_outline
        
        # For drawing a bounding box before printing.
        self.image_x_min = self.x_max
        self.image_x_max = self.x_min
        self.image_y_min = self.y_max
        self.image_y_max = self.y_min

        for i in range(3):
            self.add_comment('Setup Instructions', 'setup')
            self.add_comment('Plotting Instructions', 'plotting')
            self.add_comment('Teardown Instructions', 'teardown')

        if self.units == 'mm':
            self.setup_instructions.append('G21')
        if self.units == 'inches':
            self.setup_instructions.append('G20')

        self.setup_instructions.append(f"F{self.feed_rate}")

        self.teardown_instructions.append(SpecialInstruction.PROGRAM_END.value)

    def outline_print(self, number_of_outlines=3):
        self.add_comment('Plotting area outline', 'setup')
        for _ in range(number_of_outlines):
            self.add_special(SpecialInstruction.PEN_UP, 'setup')
            self.add_point(self.image_x_max, self.image_y_min, 'setup')
            self.add_point(self.image_x_max, self.image_y_max, 'setup')
            self.add_point(self.image_x_min, self.image_y_max, 'setup')
            self.add_point(self.image_x_min, self.image_y_min, 'setup')
            self.add_point(self.image_x_max, self.image_y_min, 'setup')

    def add_pen_down_point(self, x, y):
        self.add_special(SpecialInstruction.PEN_UP)
        self.add_special(SpecialInstruction.PAUSE)
        self.add_point(x, y)
        self.add_special(SpecialInstruction.PEN_DOWN)
        self.add_special(SpecialInstruction.PAUSE)

    def add_line(self, x1, y1, x2, y2):
        self.add_pen_down_point(x1, y1)
        self.add_point(x2, y2)

    def update_max_and_min(self, x, y):
        if x < self.image_x_min:
            self.image_x_min = x
        if x > self.image_x_max:
            self.image_x_max = x
        if y < self.image_y_min:
            self.image_y_min = y
        if y > self.image_y_max:
            self.image_y_max = y

    def add_point(self, x, y, type="plotting"):
        self.update_max_and_min(x,y)

        if (
            x > self.x_max
            or y > self.y_max
            or x < self.x_min
            or y < self.y_min
        ):
            raise ValueError("Failed to add point, outside dimensions of plotter", self.x, self.y)

        point = Point(self.feed_rate, x, y)
        
        if type == "setup":
            self.setup_instructions.append(point)
        elif type == "plotting":
            self.plotting_instructions.append(point)
        elif type == "teardown":
            self.teardown_instructions.append(point)

    def add_circle(self, x, y, radius, type="plotting"):
        self.update_max_and_min(x,y) # need to properly define the bounding box for a circle.
        pass

    def add_rectangle(self, x, y, width, height, type="plotting"):
        self.update_max_and_min(x,y) # need to properly define the bounding box for a rectangle.
        pass
        
    def add_special(self, special_instruction: SpecialInstruction, type='plotting'):
        if type == "setup":
            self.setup_instructions.append(special_instruction.value)
        elif type == 'plotting':
            self.plotting_instructions.append(special_instruction.value)
        elif type == "teardown":
            self.teardown_instructions.append(special_instruction.value)
        
    def add_comment(self, comment: str, type='plotting'):
        if type == "setup":
            self.setup_instructions.append(f";{comment}")
        elif type == 'plotting':
            self.plotting_instructions.append(f";{comment}")
        elif type == "teardown":
            self.teardown_instructions.append(f";{comment}")

    def print_to_file(self, filename: str):
        if self.should_outline:
            self.outline_print()

        with open(filename, "w") as file:
            file.write("\n".join([str(instruction) for instruction in self.setup_instructions]))
            file.write("\n")
            file.write("\n".join([str(instruction) for instruction in self.plotting_instructions]))
            file.write("\n")
            file.write("\n".join([str(instruction) for instruction in self.teardown_instructions]))

    def get(self):
        return self.plotting_instructions
 