import math
from typing import Union
from enum import Enum

# Goals
# 1. Create a class to represent a point
# 2. Create a method to check if a point is valid
# 3. Create a method to convert a point to a string
# 4. Create a grid that takes in all points and checks if they are valid
# 5. Be able to print out the grid.

from library import Instructions

def sine_wave(instructions, y_offset, amplitude):
    has_plotted_a_point = False

    instructions.add_comment(f'Sine Wave with values y_offset = {str(y_offset)} and amplitude = {str(amplitude)}')

    wavelength = 50

    # Scale up to Scale down
    scale_up = 10
    scale_down = 1 / scale_up
    for step in range(0 * scale_up, 225 * scale_up, 1):
        x = step * scale_down
        # Calculate the X and Y coordinates
        y = amplitude * math.sin((2 * math.pi * x) / wavelength)
        y += y_offset

        if has_plotted_a_point:
            instructions.add_point(x, y)     
        else:
            instructions.add_first_point(x,y)
            has_plotted_a_point = True
    return instructions

y_offset = 0.0
amplitude = 20.0

instructions = Instructions()
instructions.add_plotting_outline(number_of_outlines=1)

for i in range(0,12):
    sine_wave(instructions, y_offset - (i * 10), i)
    
instructions.print_to_file('output.gcode')