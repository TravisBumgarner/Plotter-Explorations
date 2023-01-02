from paint import main as paint
from paint_to_gcode import convert_rectangles
from arduino import send_to_arduino, receive_from_arduino, wait_for_arduino

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

    wait_for_arduino()
    for instruction in gcode:
        send_to_arduino(instruction)
        print(receive_from_arduino())


if __name__ == "__main__":
    main()
