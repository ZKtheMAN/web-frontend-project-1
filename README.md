# web-frontend-project-1

This was a project for a course on Web Front-End Engineering. This project would recommend video games for a user to check out based on their own feedback - essentially like Tinder, but for video games. The website was developed using Flask as a server-side renderer, and uses the GiantBomb REST API to gather data on the games it presents.

The original README for this project is presented below.

------------------------------------------------

GAMBLE. [Zakee Khattak, Rene Ortiz, Chukwudi Ikem] 

[Video Demonstration](https://youtu.be/-d_z2aUnDdw)

* Written for GNU/Linux (Specifically for Debian-based distributions)
* Before we get into the specific commands that you will need to get the program running, we need to get the program's source code.
* [Ctrl+Alt+T] => Shortcut to open Terminal.

* You want to create a directory (folder) somewhere on your computer. If I wish to create a folder in my documents folder I would do this.
        $ cd Documents

* Now we can clone the source code from Github into our documents folder.
        $ git clone https://github.com/349-team-5/349-project-1 
[you do not need git init, unless you wish to push this code into a new repository]
* Great! We have our code. Now you'll need pip3, flask, and a virtual environment.

* If you do not have python3.
        $ sudo apt-get install python3.8
* That should suffice, to be extra careful let's also install pip3.
        $ sudo apt-get install python3-pip
        
* You should already have pip3 upon installation of python 3.8, we can never be too sure.

* We want to create a virtual environment that will contain a copy of the Python binary, the Pip package manager , the standard Python library and other supporting files.
* We are still in our Documents folder correct? Good. Let's create a virtual environment.
        $ python3 -m venv [nameofvirtualenvironment]
[for our virtual environment, we call it virtualenv]

* Now we need to activate the virtual environment via
        $ source virtualenv/bin/activate
[you should notice your terminal change]

* Once this is done, we can verify that all software is working properly.
        $ pip install flask
[when you are inside the virtual environment you can use pip instead of pip3]
        $ python -m flask --version
        $ cd 349-project-1/vidya
        
* Alright. We can now install the required dependencies for the program to work.
        $ pip3 install -r requirements.txt
* Oh yeah, and while we are here..you will probably need a GiantBomb API_KEY.
How about we head on over to https://www.giantbomb.com/api/. Make an account, grab a key and come on back to this tutorial when you are finished.

* Finished Yet? Okay good. Now we need to provide a config file.
        $ touch config.py
        
* Open the config.py file and input your API_KEY in the format.
ex.)
	api_key="023423094209340238049234028" 
[you probably shouldn't share this value with anyone else]

* Once you have enter the api_key, have saved the file as "config.py". The last thing you need to do is. 
        $ export FLASK_APP=project
* start Flask.
        $ flask run

Packages for virtual environment

* Flask-Login: Flask-Login provides user session management for Flask. It handles the common tasks of logging in, logging out, and remembering your users’ sessions over extended periods of time

* Flask-SQLAlchemy: lask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application. It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.

* SQLite
