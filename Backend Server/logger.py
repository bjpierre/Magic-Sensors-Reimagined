from datetime import datetime
import logging
import os

date = datetime.now()
FILENAME = f"/var/log/sd2021_server/{date.month}-{date.day}-{date.year}.log"
FORMAT = "%(asctime)s -%(message)s"

if(not os.path.isfile(FILENAME)):
	os.system(f"touch {FILENAME}")

logging.basicConfig(
	filename= FILENAME,
	level=logging.INFO,
	format=FORMAT
)

def info(msg: str) -> None:
	""" Wrapper function for logging.info

	Args:
		msg (str): Message which will be logged in the log file.
	"""
	logging.info(msg)

def warning(msg: str) -> None:
	""" Wrapper function for logging.warning

	Args:
		msg (str): Message which will be logged in the log file.
	"""
	logging.warning(msg)

def error(msg: str) -> None:
	""" Wrapper function for logging.warning

	Args:
		msg (str): Message which will be logged in the log file.
	"""
	logging.error(msg)