"""
	File: main.py
	
	Function: This file acts as an entry point into the backend ecosystem.
	This file is responsible for initializing all necessary resources for
	the backend to run.
"""

import os
import sys
import psutil
import server
import logger
import tf_model_handler

__author__ = "Ryan Lanciloti"
__credits__ = ["Ryan Lanciloti"]
__version__ = "1.1.1"
__maintainer__ = "Ryan Lanciloti"
__email__ = ["ryanjl9@iastate.edu", "rlanciloti@outlook.com"]
__status__ = "Development"

def generate_pid_file() -> None:
	""" This function will generate a pid file that allows us to keep track of
	the currently active server proc. This makes it easier to kill a server 
	proc and relaunch it, or check to make sure the server is runnning.
	"""
	pid = str(os.getpid())
	pidfile = "/tmp/server_daemon.pid"

	logger.info(f"Launched Server with proc {pid}")
	server.launch_server()

	with open(pidfile, "w") as f:
		f.write(pid)

if __name__ == "__main__":
	#logger.init_logger()
	logger.info(f"App launch - Verion: {server.__version__}")

	generate_pid_file()
	tf_model_handler.init_tf_handler()

	while(True):
		pass
