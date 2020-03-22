from flask import render_template
from app import app
import pymysql
import auxFunctions as aux
import mydbconfig
from flask import render_template, flash, redirect, url_for
from app import app
import pandas as pd
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


def getMOTD():
	#msg = "Hi. I'm wimp lo, an awesome fighter!"
	#msg = "Well, I'm the chosen one"
	msg = "Rent vs Buy - CSE6242 Spring 2020"
	return msg


@app.route('/')
@app.route('/index')
def index():
    theMessage = getMOTD()
    return render_template('index.html', splashMessage=theMessage, d=pythonData, payOff=payOff)
