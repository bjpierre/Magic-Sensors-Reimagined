from flask import Flask, request
from datetime import datetime
import json
import threading
import os, sys
import logger

try:
	app = Flask(__name__)
except Exception as e:
	logger.error("Server already running - Note ignore if this was invoked by"
				 "pydoc.")

#Server IP - 10.29.163.209

version = "1.2"

@app.route("/debug/post/echo", methods=['POST'])
def _post_echo() -> str:
	""" This is a debug function which allows for a quick and simple 
	test of post functionality. If an end user want to make sure that
	their post requests are getting read by the backend server, they
	can make a post request with json that will get echoed back to 
	them. 

	Returns:
		str: The json which will be echoed back to the end user
	"""

	logger.info(f"{request.remote_addr} - Invoked post/echo")
	return request.json

@app.route("/debug/post/redeploy", methods=['POST'])
def _post_redeploy() -> None:
	""" This is a debug function which will allow for an end user to
	update and redeploy the backend server via an API call. This will
	call a script on the backend which will kill the server, pull from
	GitHub, and relaunch the server once it's finished.
	"""
	file_path = "/home/sd2021/gitRepo/Magic-Sensors-Reimagined/Backend Server"
	file_name = "redeploy_backend.py"
	os.chdir(file_path)
	logger.info(f"{request.remote_addr} - Invoked post/redeploy")
	os.system(f"python3 {file_name}")

@app.route("/debug/get/time", methods=['GET'])
def _get_time() -> str:
	""" This is a debug function that allows an end user to test GET
	requests to the server. If this function is called, it will return
	the current day and time as seen by the server.

	Returns:
		str: Current date time on the server
	"""
	d = datetime.now()
	logger.info(f"{request.remote_addr} - Invoked get/time")
	return f"{d.month}-{d.day}-{d.year} {d.hour}:{d.minute}:{d.second}"

@app.route("/debug/get/version", methods=['GET'])
def _get_version() -> str:
	""" This is a debug function that allows an end user to get the 
	current version of the backend server. The version number should 
	change with each iteration of code to prevent the use of stale code.

	Returns:
		str: Server version
	"""
	logger.info(f"{request.remote_addr} - Invoked get/version")
	return version

def launch_server():
	""" This function will launch a server on it's own thread.
	Default configuration is to launch on port 8118.
	"""
	logger.info(f"Launching Flask server running version {version}")
	threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 8118,
											"threaded": True}).start()