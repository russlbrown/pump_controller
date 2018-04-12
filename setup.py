try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'name': 'pump_controller',
	'description': 'Pump Controller for Josh\'s Friend',
	'author': 'Russ Brown',
	'author_email': 'russbrown@protonmail.com',
	'url': 'home page for the package',
	'download_url': 'Where to download it.',
	
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['pump_controller'],
	'scripts': []
	
	}

setup(**config)