---
title: Backend Wiki
author: Ryan Lanciloti
date: 10/10/2021
---

## Backend Wiki

### Sections
- [Backend Wiki](#backend-wiki)
	- [Sections](#sections)
	- [Overview](#overview)
	- [Technologies](#technologies)
	- [The Backend Code](#the-backend-code)
	- [The Docker Container](#the-docker-container)

### Overview

If you are reading this, then you've probably been told to deploy this code to server and run it/support it. If that is the case, then you're in the right place. In this file, you will find a walkthrough for each of the python files in used in the backend server, as well as how to use the docker container created to make deploying the backend that much easier.

Under the [*Technologies*](#technologies) section, you will find information on what python libraries are utilized.

Under [*The Backend Code*](#the-backend-code) section, you will find information on each python file, it's function and how it's supposed to work.

Under [*The Docker Container*](#the-docker-container) section, you will find information on how to deploy the docker container and how to support it.

### Technologies

Utilized python libraries:
- Flask (v2.0.1)
- psutils (v5.8.0)
- Tensorflow (v2.6)

Flask is the framework we are utilizing to run our custom API. It allows us to set up endpoints on our server that will run python code based on what calls are made to it.

psutils is used in the code which semi-automates deployment of the backend. As will be explained in the [*The Backend Code*](#the-backend-code) section, there is a script which will pull down the most recent version of code, kill the current server proc, and relaunch it. This will library allows us to kill that proc.

Tensorflow is the ML library that we use for training and doing inference. This is how we determine if a door is open or closed.

### The Backend Code

`File: main.py`
main.py serves as the entry point for the backend api. This has two main responsibilities: launch the flask server and generate a file which stores the process ID.

`File: server.py`
server.py is where the API endpoints are defined for the backend server. Also defined here is a class RPIServer which isn't utilized by us but can be utilized by others. Essentially, it allows for data to be fed to the backend by multiple endpoints. 

The function which will get invoked by main.py is `launch_server` which will launch flask on port 20002. It will also start the RPIServer thread manager which will remove stale servers from the list of active servers.

There are 3 over-arching endpoints: debug, server, and training. Debug endpoints serve as a way to verify that you can reach the backend, as well as manage the backend to a degree. For instance `/debug/post/redeploy` is how one would tell the server to update itself, `/debug/post/enable_logging` is how one would enable and disable logging in the backend. Server is the endpoint which would handle the Raspberry PIs serving data to the backend. Training is the endpoint used for anything machine learning. We can invoke training, get the current training status, and get the total time to train the model. (Eventually a function to invoke inference will be added as well)

`File: tf_model_handler.py`
tf_model_handler.py is where the code which handles the ML model lives. Defined in this file is also a enum which allows us to treat the handler as a finite state machine. (Hopefully more to come)

`File: logger.py`
logger.py is essentially a wrapper for the logging library in python. It includes code which allows us to specify the output file and integrates the logic to check if we should log into the wrapped logger functions.

`File: generate_pydocs.py`
This file will run generate pydocs for each of the python source files and move them to /var/ww/html where they will be accessable via an apache server. This makes creating and hosting documentation easy.

`File: server_daemon.py`
This file will act as a daemon that will check if our process is currently running (via the pid file created by main.py) and if it's not, it'll invoke the `redeploy_backend.py` script. This file is invoked by cron every minute or if the server crashes, this file will attempt to start it back up.

`File: redeploy_backend.py`
redeploy_backend.py will do 4 things: kill the current server process if it's running, pull down the most update to date code from github, call main.py, and finally generate new pydocs via the `generate_pydocs.py` file.

### The Docker Container