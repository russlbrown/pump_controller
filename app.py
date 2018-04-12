from flask import Flask
from flask import render_template
from .config import PI_PATH, DEBUG, DELAY
from time import sleep
from os import name as os_name
app = Flask(__name__)
app.debug = DEBUG
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def hello_world():
	greeting = "World"
	return render_template("index.html", greeting=greeting)


# ROUTINES
def write_to_pi(command):
	"""Send 'command' to the orange pi."""

	with open(PI_PATH, mode='w') as file:
		file.truncate()
		file.write(command)


def read_from_pi():
	"""Read from the orange pi.

	returns pump_settings dictionary"""

	with open(PI_PATH, mode='w') as file:
		file.truncate()
		file.write("R")

	sleep(DELAY)

	with open(PI_PATH, mode='r') as file:
		return file.read()[1:]


def parse_pump_settings(raw_settings):
	"""Take settings string from orange pi as a string.
	
	Return settings as a dictionary like so:
	{
		'pump1_start_pressure': <int>,   #(0 to 99)
		'pump1_stop_pressure':  <int>,   #(0 to 99)
		'pump2_start_pressure': <int>,   #(0 to 99)
		'pump2_stop_pressure':  <int>,   #(0 to 99)
		'calibration':          <int>,   #(-50 to 50)
	}
	"""
	settings = raw_settings.split(',')
	return {
		'pump1_start_pressure': settings[0],  # (0 to 99)
		'pump1_stop_pressure':  settings[1],  # (0 to 99)
	    'pump2_start_pressure': settings[2],  # (0 to 99)
	    'pump2_stop_pressure':  settings[3],  # (0 to 99)
	    'calibration':          settings[4],  # (-50 to 50)
	}


if __name__ == "__main__":
	app.run()
