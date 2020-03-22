import numpy as np

def equity_and_savings(purchase_price, down_payment, initial_rent, equity_appreciation_rate,
                       mortgage_years=30.0, mortgage_interest_rate=0.04, property_tax_rate=0.0125,
                       annual_maintenance=1000.0, annual_hoa=2000.0, annual_home_insurance=1500.0,
                       marginal_income_tax_rate=0.30, inflation_rate=0.02, savings_interest_rate=0.04,
                       closing_costs=0.05, selling_costs=0.05, number_of_months=300, debug=True):
    """
    Purpose:
    Compare equity build-up in two scenarios
    (1) Buy house with monthly mortgage payment and pay monthly fees
        (e.g., HOA, insurance, maintenance)
    (2) Pay rent every month and invest the difference in a savings (or retirement) account

    This function will calculate the net equity after sale (buy scenario) and the equity build-up
    of both scenarios for <no_months> months and return all as numpy arrays

    Inputs:
    - purchase_price (US$): Purchase price of the house (buy scenario)
    - down_payment (US$): Down payment of the house (buy scenario)
    - initial_rent (US$): Initial monthly rent (rent scenario)
    - equity_appreciation_rate (1): Annual appreciation of real estate (buy and rent scenarios)
    - mortgage_years (years): Mortgage length (e.g., 30 years) (buy scenario)
    - mortgage_interest_rate (1): Interest rate for mortgage (buy scenario)
    - property_tax_rate (1): Annual rate of property tax (buy scenario)
    - annual_maintenance (US$): Annual maintenance fees (buy scenario)
    - annual_hoa (US$): Annual payments to home owners association (buy scenario)
    - annual_home_insurance (US$): Annual insurance payments (buy scenario)
    - marginal_income_tax_rate (1): Depends on the tax bracket (buy scenario)
    - inflation_rate (1): Inflation rate used to estimate increases in annual fees (buy scenario)
    - savings_interest_rate (1): Estimated interest rate for the difference between buy and rent (rent scenario)
    - closing_costs (1): Percentage of home price that is paid when closing purchase financing (buy scenario)
    - selling_costs (1): Percentage of home price that is paid when closing sale (buy scenario)
    - number_of_months (months): Number of months to plot (buy and rent scenario)
    - debug (Boolean): Whether to print debug information
    """

    monthly_mortgage_payment = (purchase_price-down_payment) * (1.0-1.0/(1.0+mortgage_interest_rate/12.0)) \
        / ((1.0/(1.0+mortgage_interest_rate/12.0)) - (1.0/(1.0+mortgage_interest_rate/12.0)**(mortgage_years*12.0+1.0)))
    if debug:
        print('The monthly mortgage is {:.2f}'.format(monthly_mortgage_payment))
    
    # Initialize arrays
    home_value = np.zeros(number_of_months) # Current value of the house
    debt = np.zeros(number_of_months) # Current debt in mortgage account
    equity = np.zeros(number_of_months) # Current equity owned
    net_equity = np.zeros(number_of_months) # Current asset value after sale
    cash_outflow = np.zeros(number_of_months) # Total outflow of cash at the current month (buy scenario)
    rent = np.zeros(number_of_months) # Current value of rent
    savings = np.zeros(number_of_months) # Savings built up over time when renting

    # Assume that in both scenarios, we start with the money paid as down payment + closing costs
    home_value[0] = purchase_price    
    debt[0] = purchase_price-down_payment    
    equity[0] = down_payment # closing costs don't add to equity
    net_equity[0] = equity[0] - selling_costs * home_value[0]
    cash_outflow[0] = down_payment + closing_costs*(purchase_price-down_payment) # considering closing_costs
    rent[0] = initial_rent    
    savings[0] = cash_outflow[0] - rent[0]  # consider closing_costs and correct cash flow
    if debug:
        print('In month 0, the cash outflow was {:.2f}, and the rent was {:.2f}'.format(
            cash_outflow[0], rent[0]))

    for mo in range(1,number_of_months):
        ## Buy scenario
        home_value[mo] = home_value[mo-1]*(1.0+equity_appreciation_rate/12)
        # Contribution to principal
        interest_on_debt = debt[mo-1]*mortgage_interest_rate/12
        paid_principal = monthly_mortgage_payment-interest_on_debt
        
        # Total cash outflow
        insurance_payment = annual_home_insurance/12*(1.0+inflation_rate/12)**(mo-1)
        hoa_payment = annual_hoa/12*(1.0+inflation_rate/12)**(mo-1)
        maintenance_payment = annual_maintenance/12*(1.0+inflation_rate/12)**(mo-1)
        property_tax_payment = home_value[mo-1]*property_tax_rate/12
        savings_interest_deduction = (interest_on_debt+property_tax_payment)*marginal_income_tax_rate
        cash_outflow[mo] = (monthly_mortgage_payment+insurance_payment+hoa_payment+
            maintenance_payment+property_tax_payment-savings_interest_deduction)
        # Update debt and equity
        debt[mo] = debt[mo-1]-paid_principal
        equity[mo] = home_value[mo]-debt[mo]
        net_equity[mo] = equity[mo] - selling_costs * home_value[mo]
        if debug:
            print('In month {}, home value is {:.2f}, debt is {:.2f}, and equity is {:.2f}'.format(
                mo, home_value[mo], debt[mo], equity[mo]))

        ## Rent scenario
        rent[mo] = (1.0+equity_appreciation_rate/12)*rent[mo-1]
        savings[mo] = (savings[mo-1]*(1.0+savings_interest_rate/12)+
            cash_outflow[mo]-rent[mo])
        if debug:
            print('In month {}, current savings are {:.2f}'.format(mo, savings[mo]))
    
    return (equity, savings, monthly_mortgage_payment, cash_outflow, rent, net_equity)

def approximate_monthly_payments(purchase_price, down_payment, initial_rent, equity_appreciation_rate,
                       mortgage_years=30.0, mortgage_interest_rate=0.04, property_tax_rate=0.0125,
                       annual_maintenance=1000.0, annual_hoa=2000.0, annual_home_insurance=1500.0,
                       marginal_income_tax_rate=0.30, inflation_rate=0.02, savings_interest_rate=0.04,
                       closing_costs=0.05, selling_costs=0.05, number_of_months=300, debug=False):
    """
    Purpose:
    Compare equity build-up in two scenarios
    (1) Buy house with monthly mortgage payment and pay monthly fees
        (e.g., HOA, insurance, maintenance)
    (2) Pay rent every month and invest the difference in a savings (or retirement) account

    This function will calculate the average monthly outflow in the buy scenario (averaged up to the current month) and
    the current month's rent (rent scenario), returning them as numpy arrays

    Inputs:
    - purchase_price (US$): Purchase price of the house (buy scenario)
    - down_payment (US$): Down payment of the house (buy scenario)
    - initial_rent (US$): Initial monthly rent (rent scenario)
    - equity_appreciation_rate (1): Annual appreciation of real estate (buy and rent scenarios)
    - mortgage_years (years): Mortgage length (e.g., 30 years) (buy scenario)
    - mortgage_interest_rate (1): Interest rate for mortgage (buy scenario)
    - property_tax_rate (1): Annual rate of property tax (buy scenario)
    - annual_maintenance (US$): Annual maintenance fees (buy scenario)
    - annual_hoa (US$): Annual payments to home owners association (buy scenario)
    - annual_home_insurance (US$): Annual insurance payments (buy scenario)
    - marginal_income_tax_rate (1): Depends on the tax bracket (buy scenario)
    - inflation_rate (1): Inflation rate used to estimate increases in annual fees (buy scenario)
    - savings_interest_rate (1): Estimated interest rate for the difference between buy and rent (rent scenario)
    - closing_costs (1): Percentage of home price that is paid when closing purchase financing (buy scenario)
    - selling_costs (1): Percentage of home price that is paid when closing sale (buy scenario)
    - number_of_months (months): Number of months to plot (buy and rent scenario)
    - debug (Boolean): Whether to print debug information
    """
    (equity, savings, monthly_mortgage_payment, cash_outflow, rent, net_equity) = equity_and_savings(
        purchase_price, down_payment, initial_rent, equity_appreciation_rate, mortgage_years,
        mortgage_interest_rate, property_tax_rate, annual_maintenance, annual_hoa,
        annual_home_insurance, marginal_income_tax_rate, inflation_rate, savings_interest_rate,
        closing_costs, selling_costs, number_of_months, debug)
    
    monthly_buy = np.zeros(number_of_months)
    monthly_rent = np.zeros(number_of_months)
    
    for mo in range(1,number_of_months):
        monthly_buy[mo] = cash_outflow[:(mo+1)].sum()/mo
        monthly_rent[mo] = rent[mo]
    
    return (monthly_buy, monthly_rent)

def find_payback_time(purchase_price, down_payment, initial_rent, equity_appreciation_rate, number_of_months, 
                       mortgage_years=30.0, mortgage_interest_rate=0.04, property_tax_rate=0.0125,
                       annual_maintenance=1000.0, annual_hoa=2000.0, annual_home_insurance=1500.0,
                       marginal_income_tax_rate=0.30, inflation_rate=0.02, savings_interest_rate=0.04,
                       closing_costs=0.05, selling_costs=0.05, debug=False):
    """
    Purpose:
    Compare equity build-up in two scenarios
    (1) Buy house with monthly mortgage payment and pay monthly fees
        (e.g., HOA, insurance, maintenance)
    (2) Pay rent every month and invest the difference in a savings (or retirement) account

    This function will calculate the equity build-up of both scenarios for <no_months> months
    and return the number of months it will take for the buy scenario to be favorable, 
    or -1 if longer than <no_months> months

    Inputs:
    - purchase_price (US$): Purchase price of the house (buy scenario)
    - down_payment (US$): Down payment of the house (buy scenario)
    - initial_rent (US$): Initial monthly rent (rent scenario)
    - equity_appreciation_rate (1): Annual appreciation of real estate (buy and rent scenarios)
    - mortgage_years (years): Mortgage length (e.g., 30 years) (buy scenario)
    - mortgage_interest_rate (1): Interest rate for mortgage (buy scenario)
    - property_tax_rate (1): Annual rate of property tax (buy scenario)
    - annual_maintenance (US$): Annual maintenance fees (buy scenario)
    - annual_hoa (US$): Annual payments to home owners association (buy scenario)
    - annual_home_insurance (US$): Annual insurance payments (buy scenario)
    - marginal_income_tax_rate (1): Depends on the tax bracket (buy scenario)
    - inflation_rate (1): Inflation rate used to estimate increases in annual fees (buy scenario)
    - savings_interest_rate (1): Estimated interest rate for the difference between buy and rent (rent scenario)
    - closing_costs (1): Percentage of home price that is paid when closing purchase financing (buy scenario)
    - selling_costs (1): Percentage of home price that is paid when closing sale (buy scenario)
    - number_of_months (months): Number of months to plot (buy and rent scenario)
    - debug (Boolean): Whether to print debug information
    """
    (equity, savings, monthly_mortgage_payment, cash_outflow, rent, net_equity) = \
        equity_and_savings(purchase_price, down_payment, initial_rent, equity_appreciation_rate, mortgage_years,
        mortgage_interest_rate, property_tax_rate, annual_maintenance, annual_hoa,
        annual_home_insurance, marginal_income_tax_rate, inflation_rate, savings_interest_rate,
        closing_costs, selling_costs, number_of_months, debug)

    estimated_difference = net_equity - savings # changed from equity to net_equity 
    payback = -1
    for ix in range(1, len(estimated_difference)):
        if estimated_difference[ix] >= 0.0:
            payback = ix
            break
    
    return (payback, number_of_months)


if __name__ == "__main__":

    print("Running example")
    purchase_price = 420000.0
    down_payment = 20000.0
    equity_appreciation_rate = 0.02 # 3.0% -- Assumed the same for buy and rent scenarios
    initial_rent = 1600.0 # Monthly payment

    (payback, number_of_months) = find_payback_time(purchase_price, down_payment, initial_rent, equity_appreciation_rate, 120)
    if (payback < 0):
        print('It will take more than {} months to payback the investment'.format(number_of_months))
    else:
        print('It takes {} months to payback the investment'.format(payback))

else:
    print("Importing as module")