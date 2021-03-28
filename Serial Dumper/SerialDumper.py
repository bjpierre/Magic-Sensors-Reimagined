import socket
import serial
import serial.tools.list_ports

UDP_IP = "10.29.163.209"
UDP_PORT = 25565

ser = serial.Serial('COM3',115200)

ports = list(reversed(sorted(p.device for p in serial.tools.list_ports.comports())))
print(*ports, sep = ", ")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data = ser.readline(100)
    trimmed = data[0:3]
    converted = str(trimmed,"utf-8")
    if(converted.startswith('-')):
        print(converted)
        sock.sendto(converted.encode(), (UDP_IP, UDP_PORT))



