from os import name as os_name, path

# SETTINGS
DEBUG = True

BASE_DIR = path.dirname(__file__)
PI_WRITE_PATH = "/dev/ttyUSB0"
PI_READ_PATH = "/var/www/serialBuffer"
PI_WRITE_PATH_DEBUG = path.join(BASE_DIR, "pi_write_path_debug.txt")
PI_READ_PATH_DEBUG = path.join(BASE_DIR, "pi_read_path_debug.txt")
PASSWORD_PATH = path.join(path.join(BASE_DIR, "local"), "password.txt")

PRESSURE_HISTORY_PATH = "/var/www/history.csv"
CHART_PATH = path.join(path.join(BASE_DIR, "static"), "pressure_chart.svg")

# Seconds to wait from writing to the pi and reading from it.
DELAY = 0.1


# If debug is on and it is running in windows
# change file paths for testing.
if DEBUG and os_name == 'nt':
	PI_WRITE_PATH = PI_WRITE_PATH_DEBUG
	PI_READ_PATH = PI_READ_PATH_DEBUG
	PRESSURE_HISTORY_PATH = path.join(BASE_DIR, "history.csv")

