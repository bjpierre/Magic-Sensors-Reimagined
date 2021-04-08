import socket
import serial
import serial.tools.list_ports
import signal
import sys
import os

UDP_IP = "10.29.163.209"
UDP_PORT = 25565
file = open("dump.txt","w");

def signal_handler(sig, frame):
    """catches teh ctrl c singal, closes and formats dump.txt"""
    ser.close()
    file.close()
    print("Closed streams!")
    osCommandString = "notepad.exe dump.txt"
    os.system(osCommandString)
    sys.exit(0)

#hook up the signal catcher, display available serial ports, connect to our device
signal.signal(signal.SIGINT, signal_handler)
ports = list(reversed(sorted(p.device for p in serial.tools.list_ports.comports())))
print(*ports, sep = ", ")
ser = serial.Serial('COM3',115200)


##Skip the first few lines that aren't useful for our CSI data
print("Please wait", end='')
count =1
while True:
    count +=1
    data = ser.readline(50)
    if(count%2 == 0):
        print(".", end = '')
    if(str(data)[2:5] == "384"):
        break;

    
count = 0
print("\nWriting! hit ctrl+c to end, but only once, Please\nSometimes it takes a few seconds to exit!")
while True:
    
    data = ser.readline(500)
    conv = str(data)
    if(conv[2:5] == "384" or conv[2:5] == "128"):
        count +=1
        print("Matched Data :" + str(count))
        file.write(str(data)[6:-5])
        file.write("\n")
    else:
        #print("unmatched :" + str(data)[2:5])
        count = count


