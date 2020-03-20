from flask import render_template, flash, redirect, url_for
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
import auxFunctions as aux
from financialAnalysis import *

@app.route('/equity', methods=['GET', 'POST'])
def equity():
        return render_template('equity.html')
