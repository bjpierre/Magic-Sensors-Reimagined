import os
import sys
import psutil
import server
import logger

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
	logger.init_logger()
	logger.info(f"App launch - Verion: {server.version}")

	generate_pid_file()

	while(True):
		pass
