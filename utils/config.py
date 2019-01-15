import sqlite3
from os.path import dirname

MAIN_DIRECTORY = dirname(dirname(__file__))
conn = sqlite3.connect(MAIN_DIRECTORY + '/data/database.db')