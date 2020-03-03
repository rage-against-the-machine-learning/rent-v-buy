from flask import render_template
from app import app
import pymysql
import auxFunctions as aux
import mydbconfig


def getMOTD():
	#msg = "Hi. I'm wimp lo, an awesome fighter!"
	msg = "Well, I'm the chosen one"
	return msg


@app.route('/')
@app.route('/index')
def index():
    theMessage = getMOTD()
    return render_template('index.html', title='Home', errorMessage=theMessage)
