import serial
import time

arduino = serial.Serial(port="/dev/ttyS11", baudrate=9600)
print("Arduino Initialized")

def send_to_arduino(message):
    print("Sending message", message)
    arduino.write(message.encode('utf-8'))

def receive_from_arduino():
    start_marker = 60
    end_marker = 62

    message = ""
    character_received = " " 
    byte_count = -1 # to allow for the fact that the last increment will be one too many
    
    # wait for the start character
    while  ord(character_received) != start_marker: 
        character_received = arduino.read()
    
    # save data until the end marker is found
    while ord(character_received) != end_marker:
        if ord(character_received) != start_marker:
            message = message + character_received.decode("utf-8") # change for Python3
            byte_count += 1
        character_received = arduino.read()
    
    return(message)

def wait_for_arduino():   
    message = ""
    while message.find("Arduino is ready") == -1:
        while arduino.in_waiting == 0:
            pass
        
        message = receive_from_arduino()

        print (message)
        
def main():
    wait_for_arduino()
    send_to_arduino("Hello")
    
    while arduino.in_waiting == 0:
        pass
    
    message = receive_from_arduino()
    print ("Reply Received  " + message)

    arduino.close

if __name__ == "__main__":
    main()





