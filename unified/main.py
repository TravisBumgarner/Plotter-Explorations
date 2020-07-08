from paint import main as paint

"""
Steps:
1. Run paint program
2. Output paint program to Gcode
3. Send Gcode to Arduino
4. Arduino receives Gcode
5. Arduino prints what was painted
"""

def main():
    paint()

if __name__ == "__main__":
    main()
