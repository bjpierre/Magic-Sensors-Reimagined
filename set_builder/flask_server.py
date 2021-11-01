from flask import Flask, request, Response
import socket

app = Flask(__name__)

@app.route("/ml/post/inference", methods=['POST'])
def _ml_post_inference():
	global s
	string = str(request.json["payload"])
	string.strip("[]")
	stringarr = string.split()
	if(len(stringarr) != 116):
		print(f"Malformed packet: {len(stringarr)}")
		return "Failure"

	print("Good packet")
	s.send(string.encode())
	
	return "Success"


if __name__ == "__main__":
	data = None

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("localhost", 20003))

	app.run(host="0.0.0.0", port=20002)
		
