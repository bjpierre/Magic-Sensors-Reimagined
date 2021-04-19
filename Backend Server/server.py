"""
	File: server.py
	
	Function: This file handles all things API related in our backend. It's 
	job is to handle GET and PULL requests to the specified URLS, and provide
	the requested information or modify the current server state as specified
	by the request.
"""
import json
import threading
import os, sys
import logger
import time
from flask import Flask, request, Response
from datetime import datetime
import tf_model_handler

__author__ = "Ryan Lanciloti"
__credits__ = ["Ryan Lanciloti"]
__version__ = "3.1.0"
__maintainer__ = "Ryan Lanciloti"
__email__ = ["ryanjl9@iastate.edu", "rlanciloti@outlook.com"]
__status__ = "Development"

RPI_SERVERS = list()
RPI_SERVERS_LOCK = threading.Lock()

MAX_TIMEOUT = 15.0

class RPIServer:
	def __init__(self, ip_addr: str, name: str, id: str) -> None:
		self.ip_addr = ip_addr
		self.name = name
		self.id = id
		self.last_messaged = time.time()

	def toString(self) -> str:
		d = {"addr": self.ip_addr,
			 "name": self.name,
			 "id": self.id}
		return json.dumps(d)

try:
	app = Flask(__name__)
except Exception as e:
	logger.error("Server already running - Note ignore if this was invoked by"
				 "pydoc.")

#Server IP - 10.29.163.209

@app.route("/debug/post/echo", methods=['POST'])
def _debug_post_echo() -> str:
	
	""" This is a debug function which allows for a quick and simple 
	test of post functionality. If an end user want to make sure that
	their post requests are getting read by the backend server, they
	can make a post request with json that will get echoed back to 
	them. 

	:return: The json which will be echoed back to the end user
	:rtype: str
	"""

	logger.info(f"{request.remote_addr} - Invoked post/echo")
	return request.json


@app.route("/debug/post/redeploy", methods=['POST'])
def _debug_post_redeploy() -> None:
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
def _debug_get_time() -> str:
	""" This is a debug function that allows an end user to test GET
	requests to the server. If this function is called, it will return
	the current day and time as seen by the server.

	:return: Current date time on the server
	:rtype: str
	"""
	d = datetime.now()
	logger.info(f"{request.remote_addr} - Invoked get/time")
	return f"{d.month}-{d.day}-{d.year} {d.hour}:{d.minute}:{d.second}"


@app.route("/debug/get/version/server", methods=['GET'])
def _debug_get_version_server() -> str:
	""" This is a debug function that allows an end user to get the 
	current version of the backend server. The version number should 
	change with each iteration of code to prevent the use of stale code.

	:return: Server version
	:rtype: str
	"""
	logger.info(f"{request.remote_addr} - Invoked debug/get/version/server")
	return __version__


@app.route("/debug/get/version/tf_model_handler", methods=['GET'])
def _debug_get_version_tf_model_handler() -> str:
	""" This is a debug function that allows an end user to get the 
	current version of the tensorflow model handler. The version number 
	should change with each iteration of code to prevent the use of 
	stale code.

	:return: Server version
	:rtype: str
	"""
	logger.info(f"{request.remote_addr} - Invoked debug/get/version/tf_model_handler")
	return tf_model_handler.__version__


@app.route("/debug/get/exists", methods=['GET'])
def _debug_get_exists() -> (str, int):
	""" This function is for the app to check if the backend server exists. If
	the app makes this request, it can check to see if the server is answering
	requests.

	:return: Simple feedback and a 200 status code
	:rtype: (str, int)
	"""
	return ("Success", 200)


@app.route("/app/get/list_of_servers", methods=['GET'])
def _app_get_list_of_servers() -> str:
	""" Returns a list of all servers that have messaged the backend server
	within the past 15 seconds.

	:return: String list of all servers currently connected to backend
	:rtype: str
	"""
	global RPI_SERVERS
	global RPI_SERVERS_LOCK

	RPI_SERVERS_LOCK.acquire()

	l = list()
	for pi in RPI_SERVERS:
		l.append(pi.toString())
	RPI_SERVERS_LOCK.release()

	return json.dumps(l)


@app.route("/server/post/keep_alive", methods=['POST'])
def _server_post_am_alive() -> None:
	""" This function should be invoked by the Raspberry PI front end
	every 30 seconds to signal that it is still alive.
	
	------------------------------------------------------------
	NAME: This should be the name of the raspberry pi server that is 
	connected to the ESP32 reciever. This value does not need to be
	unique. This should be a string.

	ID: This should be a randomly generated, positive integer value 
	that is between 0 and 32,767. This could be made static but should
	be unique for every raspberry pi.
	
	EXAMPLE: 
		{
			"NAME" : "RPI 1",
			"ID" : 10522 
		}
	"""
	
	global RPI_SERVERS
	global RPI_SERVERS_LOCK

	try:
		body = request.json
	except json.JSONDecodeError as e:
		logger.error(f"{request.remote_addr} - {e}")
		return ("Error, not valid JSON", 400)

	if('NAME' not in body):
		logger.error(f"{request.remote_addr} - Name not provided")
		return ("Error, no name provided", 401)

	if('ID' not in body):
		logger.error(f"{request.remote_addr} - ID not provided")
		return ("Error, no id provided", 402)

	RPI_SERVERS_LOCK.acquire()

	for pi in RPI_SERVERS:
		if(pi.id == body["ID"]):
			pi.last_messaged = time.time()
			RPI_SERVERS_LOCK.release()
			return

	RPI_SERVERS.append(RPIServer(request.ip_addr, body["NAME"], body["ID"]))
	RPI_SERVERS_LOCK.release()


@app.route("/training/post/train", methods=['POST'])
def _training_post_train() -> (str, int):
	""" This is going to be the function that kicks off training. It will
	require a handful specific parameters in the JSON body.

	------------------------------------------------------------
	TYPE: String 

	if TYPE = RSSI
		DATA: List[DOOR_ANGLE][POINTS]

	if TYPE = CSI
		DATA = List[DATA_TYPE][DOOR_ANGLE][SUB_CARRIER][POINTS]
	------------------------------------------------------------
	
	TYPE: This will either be 'RSSI' or 'CSI'.
	
	SUB_CARRIER (NOTE: Only used in CSI): This will index from 0 to n-1
	where n is the total number of subcarriers we have. For our 
	implementation, it should be 32 different subcarriers, so n should
	index from 0 to 31 inclusively

	DATA_TYPE (NOTE: Only used in CSI): This will index from 0 to 1 and
	is used to denote whether or not we are adding 'Phase' data
	or 'Amplitude' data. As such, use 0 to denote 'Phase' and 1 to denote
	'Amplitude'

	DOOR_ANGLE: This will index to an integer from 0 to n-1 where n is the 
	total number of trials we spend gathering data. For instance, if we do 15 
	degree increments from 0 to 90, we will have 7 different different 
	door angles; 0, 15, 30, 45, 60, 75, 90. Thus, DOOR_ANGLE will be 
	between 0 and 6 inclusively.

	POINTS: This will index to each of the points we gather. So if we
	gather points for 30 seconds and it gives us 50 points, then this
	will index to each of those data points.

	EXAMPLE:
		{
			"TYPE" : "RSSI",
			"DATA" : [
				[0, 1, 2, 3],
				[4, 5, 6, 7],
				[8, 9, 10, 11],
				[12, 13, 14, 15],
				[16, 17, 18, 19]
			]
		}

	:return: Response: Status code letting the user know if the request was
	valid or not. 200 if okay, 400 if the JSON body doesn't contain
	the correct data.
	:rtype: tuple
	"""

	try:
		body = request.json
	except json.JSONDecodeError as e:
		logger.error(f"{request.remote_addr} - {e}")
		return ("Error, not valid JSON", 400)

	if('TYPE' not in body):
		logger.error(f"{request.remote_addr} - No type provided")
		return ("Error, no type provided", 401)

	if('DATA' not in body):
		logger.error(f"{request.remote_addr} - No data provided")
		return ("Error, no data provided", 402)

	if(str(body['TYPE']) == "RSSI"):
		tf_model_handler.DATA_TYPE = "RSSI"
		tf_model_handler.TRAINING_DATA = body["DATA"]
		tf_model_handler.STATE = tf_model_handler.MLStates.START_TRAINING

	elif(str(body['TYPE']) == "CSI"):
		tf_model_handler.DATA_TYPE = "CSI"
		tf_model_handler.TRAINING_DATA = body["DATA"]
		tf_model_handler.STATE = tf_model_handler.MLStates.START_TRAINING
	
	else:
		logger.error(f"{request.remote_addr} - Data type doesn't exist")
		return ("Error, data type specified doesn't exist", 403)

	return ("Success", 200)


@app.route("/training/get/training_status", methods=['GET'])
def _training_get_training_status() -> str:
	""" This function allows us to get the current status of the model
	training. When the training state transitions from TRAINING_IN_PROGRESS
	to FINISHED_TRAINING, the front-end server should take this as a sign
	to pull the most up-to-date model from the backend.

	:return: The current model training state. View tf_model_handler
	docs for more information on the states available.
	:rtype: str
	"""
	return tf_model_handler.STATE.name

@app.route("/training/get/training_time", methods=['GET'])
def _training_get_training_time() -> str:
	""" Once training has finished, we overwrite the training time
	variable with the new training time. This can be used as a metric
	in the app or on the front-end if desired.

	:return: Total training time in seconds 
	:rtype: str
	"""
	return str(tf_model_handler.TRAINING_TIME)


def _thread_server_manager():
	global RPI_SERVERS
	global RPI_SERVERS_LOCK
	global MAX_TIMEOUT

	RPI_SERVERS_LOCK.acquire()

	for pi in RPI_SERVERS:
		if(time.time() - pi.last_messaged > MAX_TIMEOUT):
			RPI_SERVERS.pop(pi)

	RPI_SERVERS_LOCK.release()


def launch_server():
	""" This function will launch a server on it's own thread.
	Default configuration is to launch on port 20002.
	"""
	logger.info(f"Launching Flask server running version {__version__}")
	threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 20002,
											"threaded": True}).start()