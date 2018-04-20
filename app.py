from flask import Flask
from flask import redirect, render_template, request, session
from config import PI_READ_PATH, DEBUG, DELAY, PASSWORD_PATH, PASSWORD
from config import PI_WRITE_PATH, CHART_PATH, PRESSURE_HISTORY_PATH
from time import sleep
import os
from file_read_backwards import FileReadBackwards
from datetime import datetime
import pygal
import logging.config
import yaml


# Setup Logging
def setup_logging(
    default_path='logging.yaml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


setup_logging()
app = Flask(__name__)


class PressureHistory(object):
	def __init__(self):
		self.readings = []
		with FileReadBackwards(PRESSURE_HISTORY_PATH, encoding="ASCII") as frb:
			# getting lines by lines starting from the last line up
			for reading in frb:
				columns = reading.split(',')
				self.readings.append((datetime(int(columns[0]),
	                                           int(columns[1]),
	                                           int(columns[2]),
	                                           int(columns[3]),
	                                           int(columns[4]),
	                                           int(columns[5])),
										  int(columns[6])))

				# Check if reading is older than 7 days. Stop reading from file
				# if it is.
				date_diff = (datetime.now()
				             - self.readings[-1][0]).days
				if date_diff > 7:
					self.readings = self.readings[:-1]
					break
				else:
					pass # continue collecting data

	def make_chart(self):
		line_chart = pygal.DateTimeLine(x_label_rotation=35, truncate_label=-1,
            x_value_formatter=lambda dt: dt.strftime('%d, %b %Y at %I:%M:%S %p'))
		line_chart.add('Pressure [psi]', self.readings)
		#line_chart.render_to_file(CHART_PATH)
		return line_chart.render_data_uri()


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
		return redirect('/home')
	else:
		settings = parse_pump_settings(read_from_pi())
		pressure_history = PressureHistory()
		chart = pressure_history.make_chart()
		return render_template('home.html', settings=settings, chart=chart)


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
		return file.read()


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
	app.secret_key = os.urandom(12)
	if os.name == 'nt':
		app.run(debug=DEBUG, host='127.0.0.1', port=5000)
	else:
		app.run(debug=DEBUG, host='0.0.0.0', port=80)
