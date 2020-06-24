import serial
import time

#1. (python) Send command <20, 30, 40> where the format is <X, Y, Z>


arduino = serial.Serial(port="/dev/ttyS11", baudrate=9600)
print("Arduino Initialized")

def send_to_arduino(message):
    print("Sending message", message)
    arduino.write(message.encode('utf-8'))

def receive_from_arduino():
    message = ""
    character_received = " " 

    while character_received != b'\n':
        print(character_received)
        character_received = arduino.read()
        message += character_received.decode("utf-8")
    
    return(message)

def wait_for_arduino():   
    message = ""
    while message.find("Ready") == -1:
        while arduino.in_waiting == 0:
            pass
        
        message = receive_from_arduino()

        print(message)
        
def main():
    wait_for_arduino()
    send_to_arduino("10000,30,40\n")
    
    # while arduino.in_waiting == 0:
    #     print('hello')
    #     pass
    
    message = receive_from_arduino()
    print ("Reply Received  " + message)

    arduino.close

if __name__ == "__main__":
    main()





