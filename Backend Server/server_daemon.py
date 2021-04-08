import os
import psutil

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
