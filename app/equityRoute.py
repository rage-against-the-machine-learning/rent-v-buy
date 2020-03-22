from flask import render_template, flash, redirect, url_for
from app import app
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
import auxFunctions as aux
from financialAnalysis import *

# Dummy data
payOff = 15

# Financial calcs
purchase_price = 420000.0
down_payment = 20000.0
equity_appreciation_rate = 0.02 # 3.0% -- Assumed the same for buy and rent scenarios
initial_rent = 1600.0 # Monthly payment
number_of_months = 120

equity, savings, mortgage, cash_outflow, rent, net_equity = equity_and_savings(purchase_price, down_payment, initial_rent,
                                                                         equity_appreciation_rate, number_of_months = number_of_months,
                                                                         debug=False)

df = pd.DataFrame({'month': list(range(number_of_months)),
                'buy': net_equity,
                'rent': savings})

(payOff, number_of_months) = find_payback_time(purchase_price, down_payment, initial_rent, equity_appreciation_rate, number_of_months)
pythonData = df.to_dict(orient='records')

@app.route('/equity', methods=['GET', 'POST'])
def equity():
        return render_template('equity.html', d=pythonData, payOff = payOff)