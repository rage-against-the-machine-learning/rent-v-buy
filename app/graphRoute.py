from flask import render_template, flash, redirect, url_for
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
import auxFunctions as aux
#import financialAnalysis

@app.route('/graph', methods=['GET', 'POST'])
def graph():
        return render_template('graph.html')
