from flask import render_template, request, jsonify, make_response
from app import app
import pandas as pd
from financialAnalysis import *

@app.route('/')
@app.route('/index')
def index():
    theMessage = ""
    return render_template('index.html', splashMessage=theMessage)

@app.route('/index/calculate-financials', methods=['POST'])
def calculate_financials():

    req = request.get_json()
    print("Request message was: ", req)

    # Financial calcs   
    number_of_months = 73

    # Calculate new financial results
    equity, savings, mortgage, cash_outflow, rent, net_equity = equity_and_savings(req['buyPrice'],
                                                                    req['downPayment'], req['rentPrice'],
                                                                    req['appreciationRate'], 
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
