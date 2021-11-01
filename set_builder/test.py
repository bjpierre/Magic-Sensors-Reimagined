import time
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect(("localhost", 20002))
	while(True):
		s.send(str(time.time()).encode())
		time.sleep(0.2)

	