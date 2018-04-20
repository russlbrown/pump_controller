from nose.tools import *
from .. import config
from .. import app
from random import randint


def setup():
	print("SETUP!")


def teardown():
	print("TEAR DOWN!")


def test_basic():
	print("I RAN!", end='')


def test_write_to_pi():
	command = str(randint(1, 1000))
	app.write_to_pi(command)

	with open(config.PI_WRITE_PATH_DEBUG, mode='r') as file:
		result = file.read()

	print(f"wrote to {config.PI_WRITE_PATH_DEBUG}")
	assert result == command


def test_read_from_pi():
	response = app.read_from_pi()
	assert response == "11,12,13,14,15"


def test_encode_pump_settings():
	settings = {
		'pump1_start_pressure': '1',
		'pump1_stop_pressure' : '2',
		'pump2_start_pressure': '3',
		'pump2_stop_pressure' : '4',
		'calibration'         : '5',
	}
	encoded = app.encode_settings(settings)
	print (f"encoded = {encoded}")
	assert encoded == "{S1,2,3,4,5,}"


def test_parse_pump_settings():
	chaos1 = str(randint(0, 100))
	chaos2 = str(randint(0, 100))
	chaos3 = str(randint(0, 100))
	chaos4 = str(randint(0, 100))
	chaos5 = str(randint(-50, 50))

	raw_settings = f"{chaos1},{chaos2},{chaos3},{chaos4},{chaos5},"
	parsed = app.parse_pump_settings(raw_settings)
	assert parsed['pump1_start_pressure'] == chaos1
	assert parsed['pump1_stop_pressure'] == chaos2
	assert parsed['pump2_start_pressure'] == chaos3
	assert parsed['pump2_stop_pressure'] == chaos4
	assert parsed['calibration'] == chaos5


def test_PressureHistory_init():
	pressure_history = app.PressureHistory()
	for value in pressure_history.values:
		print (value)

