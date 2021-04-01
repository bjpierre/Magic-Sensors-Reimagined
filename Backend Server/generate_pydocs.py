import os
import pydoc

def generate_pydocs():
	""" This function will generate pydocs for all python files in the project.
	It will then move the html files to the default apache2 directory.
	"""
	file_path = "/home/sd2021/gitRepo/Magic-Sensors-Reimagined/Backend Server"
	os.chdir(file_path)
	
	pyfiles = [f for f in os.listdir(".") if ".py" in f]
	for f in pyfiles:
		os.system(f"python3 -m pydoc {f} -w {f[:-3]}")
	
	os.system(f"mv *.html /var/www/html/")
	

if __name__ == "__main__":
	generate_pydocs()