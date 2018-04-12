from os import name as os_name

# SETTINGS
PI_PATH = "/dev/ttyUSB0"
PI_PATH_DEBUG = "sample_orange_pi_tty.txt"
DEBUG = True

# Seconds to wait from writing to the pi and reading from it.
DELAY = 0.1


# If debug is on and it is running in windows:
if DEBUG and os_name == 'nt':
	PI_PATH = PI_PATH_DEBUG