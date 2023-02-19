"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['Timelapse.py']
DATA_FILES = []

OPTIONS = {
	'argv_emulation': True,
	'iconfile': 'icon.icns',
	'plist': {
		'LSUIElement': True,
        'CFBundleName': "TimeLapse",
        'CFBundleDisplayName': "TimeLapse",
        'CFBundleGetInfoString': "Get shortened timelapse videos",
        'CFBundleVersion': "0.2.0",
        'CFBundleShortVersionString': "0.2.0",
        'NSHumanReadableCopyright': "© 2023 William Kaiser. All rights reserved.",
		'CFBundleShortVersionString': '0.2.0',
		'LSUIElement': True
	},
	'packages': ['cv2', 'rumps', 'mss', 'numpy']
}

setup(
	app=APP,
	name='Timelapse',
	data_files=DATA_FILES,
	options={'py2app': OPTIONS},
	setup_requires=['py2app'],
)
