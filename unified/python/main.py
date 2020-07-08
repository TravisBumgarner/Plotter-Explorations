from paint import main as paint
from paint_to_gcode import convert_rectangles

"""
Steps:
1. Run paint program
2. Output paint program to Gcode
3. Send Gcode to Arduino
4. Arduino receives Gcode
5. Arduino prints what was painted
"""


def main():
    print_instructions = paint()

    gcode_rectangles = convert_rectangles(print_instructions["rectangles"])
    gcode = [*gcode_rectangles]

    for instruction in gcode:
        print(instruction)


if __name__ == "__main__":
    main()
