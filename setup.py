from setuptools import setup

APP = ['finalGame.py']
DATA_FILES = ['PhotoP.jpg', 'PhotoR.jpg', 'PhotoQ.jpg', 'PhotoS.jpg', 'PhotoX.jpg', 'PhotoY.jpg', 'music.mp3', 'heart.jpg']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'PyQt6.QtMultimedia'],  # Add any required packages here
    'iconfile': 'tosu.icns',  # Add the custom icon file here
    'app': 'tbgf'
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
