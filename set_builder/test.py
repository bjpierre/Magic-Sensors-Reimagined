import time
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect(("localhost", 20003))
	while(True):
		tmp = []
		for i in range(255):
			tmp.append(time.time() * i)
		s.send(str(tmp).encode())
		time.sleep(0.01)

	