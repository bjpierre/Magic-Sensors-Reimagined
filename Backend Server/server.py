from flask import Flask, request
from datetime import datetime
import json
import threading

app = Flask(__name__)

@app.route("/debug/post/echo", methods=['POST'])
def post_echo():
	return request.json

@app.route("/debug/get/time", methods=['GET'])
def debug():
	d = datetime.now()
	return f"{d.month}-{d.day}-{d.year} {d.hour}:{d.minute}:{d.second}"

threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 8118, "threaded": True}).start()