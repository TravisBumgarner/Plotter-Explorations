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
    PEN_DOWN = "M3 S1000"

class Instructions:
    def __init__(self, units = 'mm', feed_rate = 10000.0, x_min = 0, x_max = 280.0, y_min = -200, y_max = 0):
        self.feed_rate = feed_rate
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.setup = []
        self.instructions = []

        if units == 'mm':
            self.setup.append('G21')
        if units == 'inches':
            self.setup.append('G20')

        self.setup.append(f"F{self.feed_rate}")

    def add_first_point(self, point: Point):
        self.instructions.append(SpecialInstruction.PEN_UP.value)
        self.instructions.append(point)
        self.instructions.append(SpecialInstruction.PEN_DOWN.value)

    def add_point(self, x, y):
        point = Point(self.feed_rate, x, y)
        
        if not self.is_point_valid(point):
            raise ValueError("Failed to add point, outside dimensions of plotter", point.x, point.y)
        
        if len(self.instructions) == 0:
            self.add_first_point(point)

        self.instructions.append(point)
        
    def add_special(self, special_instruction: SpecialInstruction):
        self.instructions.append(special_instruction.value)
            
    def is_point_valid(self, point: Point):
        if point.x > self.x_max or point.y > self.y_max or point.x < self.x_min or point.y < self.y_min:
            return False
        else:
            return True
        
    def print_to_file(self, filename: str):
        with open(filename, "w") as file:
            file.write("\n".join([str(point) for point in self.setup]))
            file.write("\n")
            file.write("\n".join([str(point) for point in self.instructions]))

    def bulk_add(self, instructions):
        self.instructions += instructions.get()

    def get(self):
        return self.instructions
 