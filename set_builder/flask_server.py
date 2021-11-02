from flask import Flask, request, Response
from rolling_average import Rolling_Average
from collections import Counter
import socket

app = Flask(__name__)

@app.route("/ml/post/inference", methods=['POST'])
def _ml_post_inference():
	global s
	global avg10
	global avg100
	global avg500

	string = str(request.json["payload"])
	open_brace_cnt = Counter(string).get("[")
	close_brace_cnt = Counter(string).get("]")
	string = string.strip("[]")
	stringarr = string.split()
	if(len(stringarr) != 106 or open_brace_cnt != 1 or close_brace_cnt != 1):
		avg10.add(0)
		avg100.add(0)
		avg500.add(0)
		print(f"Malformed packet: {len(stringarr)}")
		print(f"Last 10 Packets Success: {avg10.get_average()}")
		print(f"Last 100 Packets Success: {avg100.get_average()}")
		print(f"Last 500 Packets Success: {avg500.get_average()}")
		
		return "Failure"

	avg10.add(1)
	avg100.add(1)
	avg500.add(1)

	print("Good packet")
	print(f"Last 10 Packets Success: {avg10.get_average()}")
	print(f"Last 100 Packets Success: {avg100.get_average()}")
	print(f"Last 500 Packets Success: {avg500.get_average()}")
	s.send(string.encode())
	
	return "Success"


if __name__ == "__main__":
	data = None

	avg10 = Rolling_Average(10, 1)
	avg100 = Rolling_Average(100, 1)
	avg500 = Rolling_Average(500, 1)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("localhost", 20003))

	app.run(host="0.0.0.0", port=20002)
		
