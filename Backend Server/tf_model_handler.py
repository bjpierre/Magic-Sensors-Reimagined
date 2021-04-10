import time
import random
from enum import Enum
from threading import Thread

__author__ = "Ryan Lanciloti"
__credits__ =["Ryan Lanciloti"]
__version__ = "1.0.0"
__maintainer__ = "Ryan Lanciloti"
__email__ = ["ryanjl9@iastate.edu", "rlanciloti@outlook.com"]
__status__ = "Development"

class MLStates(Enum):
	""" This is the enum that will dictate the states that our model
	will transition through while training.

	MODEL_DOESNT_EXIST: Before we generate the model for the first time
	or if we have to delete the model for any reason, this ensures that
	the front end server doesn't accidentally try to pull non-existant 
	data.

	START_TRAINING: This state will act as a flag to kick off training
	the model. STATE will only ever be set to this state by our server
	as training has to be requested.

	TRAINING_IN_PROGRESS: While training is happening, this will act
	as a flag for both the front-end and back-end servers. If we are
	currently training, wait until it has finished.

	FINISHED_TRAINING: We will only ever enter this state once the 
	model is ready to be sent to the front-end server. When we enter
	this state, we will also set the total time that training took 
	for metrics if wanted.

	"""
	MODEL_DOESNT_EXIST = 0
	START_TRAINING = 1
	TRAINING_IN_PROGRESS = 2
	FINISHED_TRAINING = 3

""" For testing purposed, until we have a model, we're going to set
the state to FINISHED_TRAINING. Later on, when we have a model,
we will check if the model exists or not. If not, we will set the
state to MODEL_DOESNT_EXIST, otherwise FINISHED_TRAINING given
we can assume we've successfully trained the model.
"""

STATE = MLStates.MODEL_DOESNT_EXIST
TRAINING_TIME = 0
TRAINING_DATA = []
DATA_TYPE = "NOT_SET"

def _thread_training_handle():
	""" This function is responsible for handling the machine learning
	thread. This may only act as a state machine or it may be the thread
	that tensorflow runs on.
	"""
	global STATE
	global TRAINING_TIME

	tt_start = 0

	while(True):
		if STATE == MLStates.START_TRAINING:
			tt_start = time.time()
			TRAINING_TIME = 0
			STATE = MLStates.TRAINING_IN_PROGRESS
		
		if STATE == MLStates.TRAINING_IN_PROGRESS:
			time.sleep(30 + random.randint(0, 15))
			STATE = MLStates.FINISHED_TRAINING
		
		if STATE == MLStates.FINISHED_TRAINING:
			TRAINING_TIME = time.time() - tt_start


def init_tf_handler():
	""" This function will be responsible for setting up the handler. 
	Here is where we'd do the check to see if the model exists or not.
	"""

	global STATE
	global TRAINING_TIME
	global TRAINING_DATA
	global DATA_TYPE

	STATE = MLStates.FINISHED_TRAINING
	TRAINING_TIME = 0
	TRAINING_DATA = []
	DATA_TYPE = "NOT_SET"
	