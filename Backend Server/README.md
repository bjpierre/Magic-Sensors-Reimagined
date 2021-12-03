---
title: Backend Wiki
author: Ryan Lanciloti
date: 10/10/2021
---

# Backend Wiki

## Sections
- [Backend Wiki](#backend-wiki)
	- [Sections](#sections)
	- [Overview](#overview)
	- [Technologies](#technologies)
	- [The Backend Code](#the-backend-code)
	- [The Docker Container](#the-docker-container)
		- [What is it?](#what-is-it)
		- [How to use](#how-to-use)
		- [How to update](#how-to-update)
	- [Warnings/Future Improvements](#warningsfuture-improvements)

## Overview

If you are reading this, then you've probably been told to deploy this code to server and run it/support it. If that is the case, then you're in the right place. In this file, you will find a walkthrough for each of the python files in used in the backend server, as well as how to use the docker container provided to make deploying the backend that much easier.

Under the [*Technologies*](#technologies) section, you will find information on what python libraries are utilized.

Under [*The Backend Code*](#the-backend-code) section, you will find information on each python file, it's function, and how it's supposed to work.

Under [*The Docker Container*](#the-docker-container) section, you will find information on how to deploy the docker container and how to support it.

## Technologies

Utilized python libraries:
- Flask (v2.0.1)
- psutils (v5.8.0)
- Tensorflow (v2.6)

Flask is the framework we are utilizing to run our custom API. It allows us to set up endpoints on our server that will run python code based on what calls are made to it.

psutils is used in the code which semi-automates deployment of the backend. As will be explained in the [*The Backend Code*](#the-backend-code) section, there is a script which will pull down the most recent version of code, kill the current server proc, and relaunch it. This library allows us to kill that proc.

Tensorflow is the ML library that we use for training and doing inference. This is how we determine if a door is open or closed.

## The Backend Code

`File: main.py`

main.py serves as the entry point for the backend api. This has two main responsibilities: launch the flask server and generate a file which stores the process ID.


`File: server.py`

server.py is where the API endpoints are defined for the backend server. Also defined here is a class RPIServer which isn't utilized by us but can be utilized by others. Essentially, it allows for data to be fed to the backend by multiple endpoints. 

The function which will get invoked by main.py is `launch_server` which will launch flask on port 20002. It will also start the RPIServer thread manager which will remove stale end points from the list of active endpoints.

There are 4 over-arching endpoints: debug, server, training, and ml. Debug endpoints serve as a way to verify that you can reach the backend, as well as manage the backend to a degree. For instance `/debug/post/redeploy` is how one would tell the server to update itself, `/debug/post/enable_logging` is how one would enable and disable logging in the backend. Server is the endpoint which would handle the Raspberry PIs serving data to the backend. Training is the endpoint used for anything machine learning. We can invoke training, get the current training status, and get the total time to train the model. The ml endpoints are used for envoking and getting the results of inferencing.


`File: tf_model_handler.py`

tf_model_handler.py is where the code which handles the ML model lives. Defined in this file is also a enum which allows us to treat the handler as a finite state machine. With the current state of the project, the code doesn't actively build a dataset and train with it. When training is envoked, it will load in a hard-coded file which is stored in the same directory and uses that for training data. This builds a Keras classifier which will classify incoming data points based on the data it was trained with.


`File: logger.py`

logger.py is essentially a wrapper for the logging library in python. It includes code which allows us to specify the output file and integrates the logic to check if we should log into the wrapped logger functions.


`File: generate_pydocs.py`

This file will run generate pydocs for each of the python source files and move them to /var/ww/html where they will be accessable via an apache server. This makes creating and hosting documentation easy.


`File: server_daemon.py`

This file will act as a daemon that will check if our process is currently running (via the pid file created by main.py) and if it's not, it'll invoke the `redeploy_backend.py` script. This file is invoked by cron every minute and if the server crashes, this file will attempt to start it back up.


`File: redeploy_backend.py`

redeploy_backend.py will do 4 things: kill the current server process if it's running, pull down the most update to date code from github, call main.py, and finally generate new pydocs via the `generate_pydocs.py` file.

## The Docker Container

### What is it?

Docker is a means of creating a runtime environment specifically for a given application. The idea is that a developer can deploy a docker container and it's going to be a carbon copy of what the production enviornment is running in terms of packages and setup. Because this project includes multiple libraries with various dependencies and versioning issues, I have provided a docker environment that **should** run the backend server without issue exactly as we had it. One thing you may notice is that in the requirements.txt file which pip installs from, every library has been pinned to a specific version. ***I HIGHLY recommend that if any chances are made to the runtime enviornment that requires new libraries, that you also pin the version as blindly installing the newest version of a library is a good way to break your environemnt***.

### How to use

Assuming no changes to the runtime environemnt are needed, simply run the `launch_docker` script inside of the docker directory and it should set everything up. This script does two things, the first is pull down the docker container from docker hub, the second is to actually run the application. It creates a new instance of the the container with the name `sd2021` and it forwards ports 20001 and 20002 to the localhost's 20001 and 20002 respectively. When the instance is killed, it removes the container instance so the script can be reran without errors.

### How to update

So assuming updates need to be made to either the runtime config of the services or the pip modules, dockerfile, etc., the docker file will need to be rebuilt. This is the reason why I have included all of the files I used to build the container. Fair warning, the python module installation via pip takes a while. I would recommend taking the most update-to-date container, running an interactive shell, and making all necessary modifications. Test the code to verify everything still works as expected, and then update the docker file. The goal is to rebuild the docker container as little as possible.

## Warnings/Future Improvements

Firstly, I've had memory issues with the docker container eating up lots of VMem. I don't know how or why considering it's python and memory leaks *shouldn't* be possible. 

Secondly, we never tested the inferencing and training with the docker container. As it stands, with everything running on the backend server outside of a container, it's tremendously slow. I theorize it has something to do with training being done on a separate thread and it's not getting enough compute time to do training or inferencing in a reasonable amount of time. To circumvent this, consider making the inferencing module it's own process with a fork and using a shared memory space to pass data around. Unfortunately I did not get to doing this so it's up to the reader to add this. **NOTE: Not guarrenteed to work but worth a shot**.

Thirdly, I developed a partial algorithm that lives in the `csi_algorithm` folder. I ran out of time while trying to determine a good way of implementing this algorithm fully, but I theorize that it would help improve the overall accuracy of inferencing and would help determine if the dataset being used is actually useable. I included a copy of my write-up on this algorithm in the `csi_algorithm` directory.

Lastly, this project simply may not be possible. While detecting the state of a door using CSI is possible in theory, there are a lot of factors that makes it incredibly difficult, if not impossible to do in practice. From the transmission power of the ESP32s to the shifting of metal or water-based objects in a room, all of these are factors which can affect the data seen by the reciever. We were unable to build a dataset which proved the feasibility of the project. **I would highly recommend starting out by gathering datasets sets at various locations and verifying that the data is consisent at different door angles and that it's distinct between your different angle markers**. Good luck and hopefully you found some value in this guide.