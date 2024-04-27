import sqlite3 # sqlite3 does not have a __version__ attribute.
import flask
import werkzeug
import flask_restful_swagger
import flask_restful

libList = [flask, werkzeug]

for lib in libList :
    print("pip install %s == %s"%(lib.__name__, lib.__version__))


