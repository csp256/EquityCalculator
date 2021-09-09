##################################################################### This calculator is for computing leveraged equity growth.
#
# It ignores cashflows from the financed asset, but assumes
# that the cashflow pays for all costs, including financing.
#
# It only tracks equity from appreciation and principal paydown.
###################################################################

# Loan
down_payment = 0.03 # 0.03 means 3%
interest_rate = 0.04
term = 30 # years

# Trends
appreciation_rate = 0.02
inflation_rate = 0.02 # typically same as appreciation rate

###################################################################
# Edit only the variables above. 
###################################################################

import numpy_financial as npf
import matplotlib.pyplot as plt

months = term * 12
monthly_rate = interest_rate / 12.
initial_debt = 1.0 - down_payment

monthly_payment = -npf.pmt(monthly_rate, months, initial_debt)

month_list = [i for i in range(months + 1)]
year_list = [i / 12. for i in month_list]

def balance_remaining(payment, monthly_rate, months_remaining):
  return (payment / monthly_rate) * (1. - (1. / (1. + monthly_rate))**months_remaining)

debt = [balance_remaining(monthly_payment, monthly_rate, months - i) for i in month_list]
base_equity = [1. - i for i in debt]

appreciation = [(1. + appreciation_rate)**(i/12.) - 1. for i in month_list]

equity = [base_equity[i] + appreciation[i] for i in month_list] 
real_equity = [equity[i] / ((1. + inflation_rate)**(i/12.)) for i in month_list]

title = '\ninterest: ' + str(100.*interest_rate) + '% term: ' + str(term) + 'yr down: ' + str(100.*down_payment) + '%\nappreciation: ' + str(100.*appreciation_rate) + '% inflation: ' + str(100.*inflation_rate) + '%'

def pcnt(x):
  return [100.*i for i in x]

plt.clf()
plt.plot(year_list, pcnt(equity))
plt.plot(year_list, pcnt(real_equity))
plt.legend(['nominal', 'real'])
plt.grid('both')
plt.xlabel('Year')
plt.ylabel('Equity [Purchase Price %]')
plt.title(title)
plt.savefig('equity.png')

def in_downpayments(x):
  return [i/down_payment for i in x]

plt.clf()
plt.plot(year_list, in_downpayments(equity))
plt.plot(year_list, in_downpayments(real_equity))
plt.legend(['nominal', 'real'])
plt.grid('both')
plt.xlabel('Year')
plt.ylabel('Equity [Down Payments]')
plt.title(title)
plt.savefig('down_payments.png')

ltv = [(appreciation[i] + base_equity[i]) / (appreciation[i] + 1.)  for i in month_list]

plt.clf()
plt.plot(year_list, pcnt(ltv))
plt.grid('both')
plt.yticks([5*i for i in range(21)])
plt.xlabel('Year')
plt.ylabel('Loan to Value [%]')
plt.title(title)
plt.savefig('LTV.png')

def rate_of_return(x):
  return [(x[i+1] - x[i])/x[i] for i in range(len(x) - 1)]
def annualize(x):
  return [(1. + i)**12 - 1. for i in x]
ROR = annualize(rate_of_return(equity))

def average(x):
  return [(x[i+1] + x[i]) / 2. for i in range(len(x) - 1)]
year_list_avg = average(year_list)

plt.clf()
plt.plot(year_list_avg, pcnt(ROR))
plt.grid('both')
plt.xlabel('Year')
plt.ylabel('Instantaneous Rate of Return [%]')
plt.title(title)
plt.savefig('rate_of_return.png')

def CAGR(x):
  return [(equity[i] / down_payment)**(1./(i/12.)) - 1. for i in month_list[1:]]
ROE = CAGR(equity)

def add_constant(x, c):
  return [i+c for i in x]
real_ROE = add_constant(ROE, -inflation_rate)

plt.clf()
plt.plot(year_list[1:], pcnt(ROE))
plt.plot(year_list[1:], pcnt(real_ROE))
plt.legend(['nominal', 'real'])
plt.grid('both')
plt.xlabel('Year')
plt.ylabel('Compound Annual Growth Rate [%]')
plt.title(title)
plt.savefig('CAGR_auto.png')
plt.ylim([0., 50.])
plt.yticks([5*i for i in range(11)])
plt.savefig('CAGR_fixed.png')

