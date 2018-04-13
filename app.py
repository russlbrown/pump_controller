from flask import Flask
from flask import flash, redirect, render_template, request, session, abort
from config import PI_READ_PATH, DEBUG, DELAY, PASSWORD_PATH, PASSWORD
from config import PI_WRITE_PATH
from time import sleep
from os import name as os_name, urandom


app = Flask(__name__)


@app.route('/')
def index():
	if not session.get('logged_in'):
		return redirect('/login')
	else:
		return redirect('/home')


@app.route('/home', methods=['POST', 'GET'])
def home():
	if not session.get('logged_in'):
		return redirect('/login')
	else:
		pass

	if request.method == 'POST':
		settings = {
			'pump1_start_pressure': request.form['pump1_start_pressure'],
			'pump1_stop_pressure': request.form['pump1_stop_pressure'],
			'pump2_start_pressure': request.form['pump2_start_pressure'],
			'pump2_stop_pressure': request.form['pump2_stop_pressure'],
			'calibration': request.form['calibration'],
			}
		write_to_pi(encode_settings(settings))
		return render_template('home.html', settings=settings)
	else:
		settings = parse_pump_settings(read_from_pi())
		return render_template('home.html', settings=settings)


@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
	if request.method == 'POST':
		if request.form['password'] == PASSWORD and request.form[
			'username'] == 'admin':
			session['logged_in'] = True
			return redirect('/home')
		else:
			return render_template('message.html', message='Wrong password!')
	else:
		return render_template('login.html')


@app.route("/logout")
def logout():
	session['logged_in'] = False
	return home()


# ROUTINES
def write_to_pi(command):
	"""Send 'command' to the orange pi."""

	with open(PI_WRITE_PATH, mode='w') as file:
		file.write(command)


def read_from_pi():
	"""Read from the orange pi.

	returns pump_settings dictionary"""

	#with open(PI_READ_PATH, mode='w') as file:
	#	file.truncate()

	with open(PI_WRITE_PATH, mode='w') as file:
		file.write("{R}")

	sleep(DELAY)

	with open(PI_READ_PATH, mode='r') as file:
		return file.read()[1:]


def encode_settings(settings):
	return ("{S"
            + settings['pump1_start_pressure'] + ","
			+ settings['pump1_stop_pressure'] + ","
			+ settings['pump2_start_pressure'] + ","
			+ settings['pump2_stop_pressure'] + ","
			+ settings['calibration'] + ","
			+ "}"
           )


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
	app.secret_key = urandom(12)
	if os_name == 'nt':
		app.run(debug=DEBUG, host='127.0.0.1', port=5000)
	else:
		app.run(debug=DEBUG, host='0.0.0.0', port=80)
