"""
	File: set_builder_server.py
	
	Function: This file acts as a server which can be used to build a training
	data set. Important things to note:

"""
import socket
import os
import random
import time
import copy
from threading import Thread
from enum import Enum

PORT = 20002
WAIT_TIME = 5.0

class AppSM (Enum):
	WAIT_FOR_START = 1
	GATHER_DATA = 2
	DONE = 3

class FileWriter:

	def __init__(self, fdir, prefix):
		self.fdir = fdir
		self.prefix = prefix
		self.file = None

		self.make_dir()

	
	def make_dir(self):
		exists = os.path.isdir(self.fdir)
		if not exists:
			os.mkdir(self.fdir)

	def open_next_file(self, file_name):
		self.close_file()
		
		iter = 0

		path = f"{self.fdir}/{self.prefix}{iter}_{file_name}"

		while(os.path.exists(path)):
			path = f"{self.fdir}/{self.prefix}{iter}_{file_name}"
			iter += 1
		
		self.file = open(path, "w")

	def write_line(self, data: str):
		if(self.file == None): return
		if(data == None): return

		self.file.write(data + "\n")

	def close_file(self):
		if(self.file == None): return
		self.file.close()


class Server:
	def __init__(self, port=PORT):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.port = port
		self.conn = None
		self.data = None
		self.has_data = False

		self.create_server()

		print("Waiting for client to connect...")
		self.wait_for_connection()

	def create_server(self):
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(("localhost", self.port))

	def wait_for_connection(self):
		self.sock.listen(1)
		self.conn, addr = self.sock.accept()

	def get_data(self):
		if self.conn == None:
			return None

		self.data = self.conn.recv(1024).decode("utf-8").strip("\n")
		if(self.data != None):
			self.has_data = True

	def consume(self):
		self.has_data = False
		tmp = copy.deepcopy(self.data)
		self.data = None
		return tmp


def test_fw():
	fw = FileWriter("output", "test_file_")

	for i in range(6):
		fw.open_next_file(f"{i}_angle")
		for j in range(20):
			arr = []
			for k in range(120):
				arr.append(random.randint(0,255))
			fw.write_line(str(arr))
	
	fw.close_file()


def thread_func():
	global s
	global sm
	while(sm != AppSM.DONE):
		s.get_data()


def test_server():
	global s
	global sm

	s = Server()

	print("Client Connected - Waiting for data...")

	t = Thread(target=thread_func, args=())
	t.start()

	data = ""
	while(data != "q"):
		if s.has_data:
			data = s.consume()
			print(data)


if __name__ == '__main__':
	s = Server()
	sm = AppSM.WAIT_FOR_START

	fw = FileWriter("output", "set_data_")
	print("Client Connected - Waiting for data...")

	t = Thread(target=thread_func, args=())
	t.start()

	angles = [0, 15, 30, 45, 60, 75, 90]

	cmd = ""
	angle = 0

	for angle in angles:
		print(f"Waiting to gather data for angle {angle}")

		while(cmd != "next"):
			cmd = input(">> ")
		cmd = ""

		stime = time.time()
		fw.open_next_file(f"{angle}_degree")
		print(f"Gathering data points for angle {angle}")

		while(time.time() - stime < WAIT_TIME):
			fw.write_line(s.consume())

	fw.close_file()
	sm = AppSM.DONE


