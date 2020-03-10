import numpy as np

def approximate_equity_and_savings(purchase_price, down_payment, initial_rent, 
        equity_appreciation, mortgage_length=30, mortgage_interest_rate=0.06, property_tax_rate=0.0125,
        maintenance_fees=1000.0, hoa_fees=2000.0, insurance_fees=1500.0, 
        marginal_income_tax_rate = 0.30, inflation=0.02, savings_interest_rate = 0.06,
        no_months=20*12):
    """
    Purpose:
    Compare equity build-up in two scenarios
    (1) Buy house with monthly mortgage payment and pay monthly fees
        (e.g., HOA, insurance, maintenance)
    (2) Pay rent every month and invest the difference in a savings (or retirement) acct

    This function will calculate the equity build-up of both scenarios for <no_months> months
    and return both as numpy arrays

    Inputs:
    - purchase_price (US$): Purchase price of the house (buy scenario)
    - down_payment (US$): Down payment of the house (buy scenario)
    - initial_rent (US$): Initial monthly rent (rent scenario)
    - equity_appreciation (1): Annual appreciation of real estate (buy and rent scenarios)
    - mortgage_length (years): Mortgage length (e.g., 30 years) (buy scenario)
    - mortgage_interest_rate (1): Interest rate for mortgage (buy scenario)
    - property_tax_rate (1): Annual rate of property tax (buy scenario)
    - maintenance_fees (US$): Annual maintenance fees (buy scenario)
    - hoa_fees (US$): Annual payments to home owners association (buy scenario)
    - insurance_fees (US$): Annual insurance payments (buy scenario)
    - marginal_income_tax_rate (1): Depends on the tax bracket (buy scenario)
    - inflation (1): Inflation rate used to estimate increases in annual fees (buy scenario)
    - savings_interest_rate (1): Estimated interest rate for the difference between buy and rent (rent scenario)
    - no_months (months): Number of months to plot (buy and rent scenario)
    """

    monthly_mortgage_payment = ((purchase_price-down_payment)*(1.0-1.0/(1.0+mortgage_interest_rate/12))
        /(1.0-1.0/(1.0+mortgage_interest_rate/12)**(mortgage_length*12+1)))

    home_value = np.zeros(no_months)
    debt = np.zeros(no_months)
    equity = np.zeros(no_months)
    cash_outflow = np.zeros(no_months)
    rent = np.zeros(no_months)
    savings_when_renting = np.zeros(no_months)

    home_value[0] = purchase_price    
    debt[0] = purchase_price-down_payment    
    equity[0] = down_payment    
    cash_outflow[0] = down_payment    
    rent[0] = initial_rent    
    savings_when_renting[0] = down_payment

    for mo in range(1,no_months):

        ## Buy scenario
        home_value[mo] = home_value[mo-1]*(1.0+equity_appreciation/12)
        # Contribution to principal
        interest_on_debt = debt[mo-1]*mortgage_interest_rate/12
        paid_principal = monthly_mortgage_payment-interest_on_debt
        # Total cash outflow
        insurance_payment = insurance_fees/12*(1.0+inflation/12)**mo
        hoa_payment = hoa_fees/12*(1.0+inflation/12)**mo
        maintenance_payment = maintenance_fees/12*(1.0+inflation/12)**mo
        property_tax_payment = home_value[mo-1]*property_tax_rate/12
        savings_interest_deduction = (interest_on_debt+property_tax_payment)*marginal_income_tax_rate
        cash_outflow[mo] = monthly_mortgage_payment+insurance_payment+hoa_payment+maintenance_payment+property_tax_payment-savings_interest_deduction
        # Update debt and equity
        debt[mo] = debt[mo-1]-paid_principal
        equity[mo] = home_value[mo]-debt[mo]

        ## Rent scenario
        rent[mo] = (1.0+equity_appreciation/12)*rent[mo-1]
        savings_when_renting[mo] = savings_when_renting[mo-1]*(1.0+savings_interest_rate/12)+cash_outflow[mo]-rent[mo]
    
    return (equity, savings_when_renting)

def calculate_npv(purchase_price, down_payment, initial_rent,
        equity_appreciation, mortgage_length=30, mortgage_interest_rate=0.06, property_tax_rate=0.0125,
        maintenance_fees=1000.0, hoa_fees=2000.0, insurance_fees=1500.0, 
        marginal_income_tax_rate = 0.30, inflation=0.02, savings_interest_rate = 0.06,
        no_months=20*12, sale_comission=0.06):
    """
    Purpose:
    Calculate the net cash if house is held for <no_months> months and then sold
    Compare to the savings obtained if renting for <no_months>
    Discount the difference between the two (i.e., the NPV of the benefit of owning vs. renting)

    Inputs (new ones only):
    - sale_comission (1): Transaction cost of selling house as ratio of house price
    """
    #TODO

    return False

def find_payback_time(purchase_price, down_payment, initial_rent, 
        equity_appreciation, mortgage_length=30, mortgage_interest_rate=0.06, property_tax_rate=0.0125,
        maintenance_fees=1000.0, hoa_fees=2000.0, insurance_fees=1500.0, 
        marginal_income_tax_rate = 0.30, inflation=0.02, savings_interest_rate = 0.06,
        no_months=20*12):
    """
    Purpose:
    Estimate from which month it becomes a better decision to buy a house than to rent
    """
    estimated_equity, estimated_savings = approximate_equity_and_savings(
            purchase_price, down_payment, initial_rent, equity_appreciation)
    estimated_difference = estimated_equity-estimated_savings

    payback = estimated_difference.shape[0]
    for ix in range(1,estimated_difference.shape[0]):
        if estimated_difference[ix] <= 0.0:
            payback = ix
            break

    return payback   


if __name__ == "__main__":

    print("Running example")
    purchase_price = 725000.0
    down_payment = 100000.0
    equity_appreciation = 0.03 # 3.0% -- Assumed the same for buy and rent scenarios
    initial_rent = 1950.0 # Monthly payment

    payback = find_payback_time(purchase_price, down_payment, initial_rent, equity_appreciation)
    print('Owning is better than renting if staying more than ', payback, ' months')

else:
    print("Importing as module")