from datetime import datetime
import logging

FORMAT = "%(asctime)s -%(message)s"
logging.basicConfig(
	filename= "/var/logs/sd2021_server/{date.month}-{date.day}-{date.year}.log",
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