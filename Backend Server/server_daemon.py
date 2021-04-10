"""
	File: server_daemon.py
	
	Function: This file acts as a watchdog process that checks to see if the server
	is still running or if it died. It's assumed that if the server proc died, that
	there was a bad code change pushed. Because of this assumption, this file will
	invoke redeploy_backend.py to ensure that if we relaunch the server, it's the 
	most up-to-date version, as specified by github. 

	This file is called every 5 minutes by a cronjob on the back-end. That means that
	the server shouldn't be down for more than 5 minutes at any given point if the 
	code which exists in git is functional.
"""

import os
import psutil

__author__ = "Ryan Lanciloti"
__credits__ = ["Ryan Lanciloti"]
__version__ = "1.5.0"
__maintainer__ = "Ryan Lanciloti"
__email__ = ["ryanjl9@iastate.edu", "rlanciloti@outlook.com"]
__status__ = "Development"

def check_main_pid() -> None:
	""" This function will check to see if the server is still running. If it's not,
	then it probably crashed from a bad code push. Run the redeploy script which will
	update the code and attempt to relaunch the server.
	"""
	pidfile = "/tmp/server_daemon.pid"
	file_path = "/home/sd2021/gitRepo/Magic-Sensors-Reimagined/Backend Server"
	file_name = "redeploy_backend.py"

	if os.path.isfile(pidfile):
		with open(pidfile, "r") as f:
			pid = int(f.readline())
			if not psutil.pid_exists(pid):
				os.chdir(file_path)
				os.system(f"python3 {file_name}")
	else:
		os.chdir(file_path)
		os.system(f"python3 {file_name} &")


if __name__ == "__main__":
    check_main_pid()
