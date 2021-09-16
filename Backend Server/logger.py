"""
	File: logger.py
	
	Function: This file as a wrapper for the "logging" library in python.
	Having this wrapper allows us to initialize the how we'd like the logger
	to log events.
"""

from datetime import datetime
import logging
import os

__author__ = "Ryan Lanciloti"
__credits__ = ["Ryan Lanciloti"]
__version__ = "1.0.7"
__maintainer__ = "Ryan Lanciloti"
__email__ = ["ryanjl9@iastate.edu", "rlanciloti@outlook.com"]
__status__ = "Development"

LOGGING_ENABLED = False

def init_logger():
	""" This function will initalize our logger to write a log file to 
	/var/log/sd2021/ for ease of debugging later on.
	"""
	date = datetime.now()
	FILENAME = f"/var/log/sd2021_server/{date.month}-{date.day}-{date.year}.log"
	FORMAT = "%(asctime)s - %(message)s"

	if(not os.path.isfile(FILENAME)):
		os.system(f"touch {FILENAME}")

	logging.basicConfig(
		filename= FILENAME,
		level=logging.INFO,
		format=FORMAT
	)

def info(msg: str) -> None:
	""" Wrapper function for logging.info

	:param msg: Message which will be logged in the log file.
	:type msg: str
	"""
	logging.info(msg) if LOGGING_ENABLED

def warning(msg: str) -> None:
	""" Wrapper function for logging.warning

	:param msg: Message which will be logged in the log file.
	:type msg: str
	"""
	logging.warning(msg) if LOGGING_ENABLED

def error(msg: str) -> None:
	""" Wrapper function for logging.error

	:param msg: Message which will be logged in the log file.
	:type msg: str
	"""
	logging.error(msg) if LOGGING_ENABLED