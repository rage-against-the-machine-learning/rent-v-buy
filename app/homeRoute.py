from flask import render_template
from app import app
import pymysql
import auxFunctions as aux
import mydbconfig
from flask import render_template, flash, redirect, url_for, request, jsonify, make_response
from app import app
import pandas as pd
from financialAnalysis import *

def getMOTD():
	#msg = "Hi. I'm wimp lo, an awesome fighter!"
	#msg = "Well, I'm the chosen one"
	msg = "Rent vs Buy - CSE6242 Spring 2020"
	return msg


@app.route('/')
@app.route('/index')
def index():
    theMessage = getMOTD()
    return render_template('index.html', splashMessage=theMessage)

@app.route('/index/calculate-financials', methods=['POST'])
def calculate_financials():

    req = request.get_json()
    print("Request message was: ", req)

    # Financial calcs
    purchase_price = 420000.0
    equity_appreciation_rate = 0.02 # 3.0% -- Assumed the same for buy and rent scenarios
    initial_rent = 1600.0 # Monthly payment
    
    number_of_months = 121

    # Calculate new financial results
    equity, savings, mortgage, cash_outflow, rent, net_equity = equity_and_savings(purchase_price,
                                                                    req['downPayment'], initial_rent,
                                                                    equity_appreciation_rate, 
                                                                    mortgage_interest_rate = req['mortgageRate']/100.0,
                                                                    annual_maintenance = req['maintenance'],
                                                                    annual_home_insurance = req['homeInsurance'],
                                                                    mortgage_years = req['mortgageHorizon'],
                                                                    number_of_months = number_of_months,
                                                                    debug=False)
    
    data = pd.DataFrame({'month': list(range(number_of_months)),
                'buy': net_equity,
                'rent': savings}).to_dict(orient='records')
    
    (payOff, _) = find_payback_time(net_equity, savings, number_of_months)
    #print("This time it takes ", payOff)

    res = make_response(jsonify({"payOff": payOff,
                        "data": data}), 200)

    return res
