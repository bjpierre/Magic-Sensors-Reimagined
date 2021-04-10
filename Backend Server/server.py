import json
import threading
import os, sys
import logger
from flask import Flask, request, Response
from datetime import datetime
import tf_model_handler

__author__ = "Ryan Lanciloti"
__credits__ =["Ryan Lanciloti"]
__version__ = "2.0.0"
__maintainer__ = "Ryan Lanciloti"
__email__ = ["ryanjl9@iastate.edu", "rlanciloti@outlook.com"]
__status__ = "Development"

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

	Returns:
		str: The json which will be echoed back to the end user
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

	Returns:
		str: Current date time on the server
	"""
	d = datetime.now()
	logger.info(f"{request.remote_addr} - Invoked get/time")
	return f"{d.month}-{d.day}-{d.year} {d.hour}:{d.minute}:{d.second}"

@app.route("/debug/get/version/server", methods=['GET'])
def _debug_get_version() -> str:
	""" This is a debug function that allows an end user to get the 
	current version of the backend server. The version number should 
	change with each iteration of code to prevent the use of stale code.

	Returns:
		str: Server version
	"""
	logger.info(f"{request.remote_addr} - Invoked debug/get/version/server")
	return __version__

@app.route("/debug/get/version/tf_model_handler", methods=['GET'])
def _debug_get_version() -> str:
	""" This is a debug function that allows an end user to get the 
	current version of the tensorflow model handler. The version number 
	should change with each iteration of code to prevent the use of 
	stale code.

	Returns:
		str: Tensorflow model handler version
	"""
	logger.info(f"{request.remote_addr} - Invoked debug/get/version/tf_model_handler")
	return tf_model_handler.__version__


@app.route("/training/post/train", methods=['POST'])
def _training_post_train() -> (str, int):
	""" This is going to be the function that kicks off training. It will
	require a handful specific parameters in the JSON body.

	------------------------------------------------------------
	TYPE: String 

	if TYPE = RSSI
		DATA: List[DOOR_ANGLE][POINTS]

	if TYPE = CSI
		DATA = List[SUB_CARRIER][DATA_TYPE][DOOR_ANGLE][POINTS]
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

	Returns:
		Response: Status code letting the user know if the request was
		valid or not. 200 if okay, 400 if the JSON body doesn't contain
		the correct data.
	"""

	try:
		body = json.loads(request.json())
	except json.JSONDecodeError as e:
		logger.error(f"{request.remote_addr} - {e}")
		return ("Error, not valid JSON", 400)

	if(not str(body['TYPE'])):
		logger.error(f"{request.remote_addr} - {e}")
		return ("Error, no type provided", 401)

	if(not body['DATA']):
		logger.error(f"{request.remote_addr} - {e}")
		return ("Error, no data provided", 402)

	if(str(body['TYPE']) == "RSSI"):
		tf_model_handler.DATA_TYPE = "RSSI"
		tf_model_handler.TRAINING_DATA = body["DATA"]
		tf_model_handler.STATE = tf_model_handler.MLStates.TRAINING_IN_PROGRESS

	elif(str(body['TYPE']) == "CSI"):
		tf_model_handler.DATA_TYPE = "CSI"
		tf_model_handler.TRAINING_DATA = body["DATA"]
		tf_model_handler.STATE = tf_model_handler.MLStates.TRAINING_IN_PROGRESS
	
	else:
		logger.error(f"{request.remote_addr} - {e}")
		return ("Error, data type specified doesn't exist", 403)

	return ("Success", 200)


@app.route("/training/get/training_status", methods=['GET'])
def _training_get_training_status() -> str:
	""" This function allows us to get the current status of the model
	training. When the training state transitions from TRAINING_IN_PROGRESS
	to FINISHED_TRAINING, the front-end server should take this as a sign
	to pull the most up-to-date model from the backend.

	Returns:
		str: The current model training state. View tf_model_handler
		docs for more information on the states available.
	"""
	return tf_model_handler.STATE.name

@app.route("/training/get/training_time", methods=['GET'])
def _training_get_training_status() -> float:
	""" Once training has finished, we overwrite the training time
	variable with the new training time. This can be used as a metric
	in the app or on the front-end if desired.

	Returns:
		float: Total training time in seconds 
	"""
	return tf_model_handler.TRAINING_TIME


def launch_server():
	""" This function will launch a server on it's own thread.
	Default configuration is to launch on port 8118.
	"""
	logger.info(f"Launching Flask server running version {__version__}")
	threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 8118,
											"threaded": True}).start()