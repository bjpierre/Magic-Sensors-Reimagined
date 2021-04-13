"""
	File: generate_pydocs.py
	
	Function: This file will get invoked by redeploy_backened.py and is how
	we will autogenerate HTML documentation for our backend. Once documentation
	is generated, it will move it to /var/www/html so that when a user goes to
	"server_ip:20001/", they are greated with a list of all the files and the 
	documentation for their functions.
"""

import os
import pydoc

__author__ = "Ryan Lanciloti"
__credits__ = ["Ryan Lanciloti"]
__version__ = "1.0.6"
__maintainer__ = "Ryan Lanciloti"
__email__ = ["ryanjl9@iastate.edu", "rlanciloti@outlook.com"]
__status__ = "Development"

def generate_pydocs():
	""" This function will generate pydocs for all python files in the project.
	It will then move the html files to the default apache2 directory.
	"""
	file_path = "/home/sd2021/gitRepo/Magic-Sensors-Reimagined/Backend Server"
	os.chdir(file_path)
	
	pyfiles = [f for f in os.listdir(".") if ".py" in f]
	for f in pyfiles:
		os.system(f"python3 -m pydoc -w {f[:-3]}")
	
	os.system(f"mv *.html /var/www/html/")
	

if __name__ == "__main__":
	generate_pydocs()