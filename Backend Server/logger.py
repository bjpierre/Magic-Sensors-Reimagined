from datetime import datetime
import logging
import os

FILENAME = "/var/logs/sd2021_server/{date.month}-{date.day}-{date.year}.log"
FORMAT = "%(asctime)s -%(message)s"

if(not os.path.isfile(FILENAME)):
	os.system(f"touch {FILENAME}")

logging.basicConfig(
	filename= FILENAME,
	level=logging.INFO,
	format=FORMAT
)

def info(msg: str, *args, **kwargs) -> None:
	""" Wrapper function for logging.info

	Args:
		msg (str): Message which will be logged in the log file.
	"""
	logging.info(msg, args, kwargs)

def warning(msg: str, *args, **kwargs) -> None:
	""" Wrapper function for logging.warning

	Args:
		msg (str): Message which will be logged in the log file.
	"""
	logging.warning(msg, *args, **kwargs)

def error(msg: str, *args, **kwargs) -> None:
	""" Wrapper function for logging.warning

	Args:
		msg (str): Message which will be logged in the log file.
	"""
	logging.error(msg, *args, **kwargs)