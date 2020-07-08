import serial
import time

from config import ARDUINO_PORT, ARDUINO_BAUD_RATE

arduino = serial.Serial(port=ARDUINO_PORT, baudrate=ARDUINO_BAUD_RATE)


def send_to_arduino(message):
    print("Sending message", message)
    message = f"{message}\n"
    arduino.write(message.encode("utf-8"))


def receive_from_arduino():
    message = ""
    character_received = " "

    while character_received != b"\n":
        character_received = arduino.read()
        message += character_received.decode("utf-8")

    return message


def wait_for_arduino():
    message = ""
    while message.find("Ready") == -1:
        while arduino.in_waiting == 0:
            pass

        message = receive_from_arduino()

        print(message)


# def main():
#     wait_for_arduino()
#     send_to_arduino("10000,30,40\n")

#     message = receive_from_arduino()
#     print ("Reply Received  " + message)

#     arduino.close

# if __name__ == "__main__":
#     main()

