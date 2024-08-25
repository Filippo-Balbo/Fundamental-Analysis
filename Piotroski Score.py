#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 16:41:02 2024

@author: filippobalbo
"""

import yahoo_1in.stock_info as yf
import pandas as pd
import time 

balance_sheet = []
income_stat = []
cfs = []
years = []

BS = []
I = []
CF = []
Y = []

profitability_score = 0
leverage_score = 0
operating_efficiency_score = 0
pe_ratio = 0

summary = pd.DataFrame(columns = ['TICKER', 'PE RATIO', 'PROFITABILITY', 'LEVERAGE', 'OPERATING EFFICIENCY'])

tickers = yf.tickers_sp500()
sp500_list = [(idx, item) for idx,item in enumerate(tickers)]
#tickers_list = pd.DataFrame(tickers_list)
print (sp500_list)
print()

# Get Data:
def company_data(company):
    global BS
    global I
    global CF
    global Y
    BS = yf.get_balance_sheet(company)
    I = yf.get_income_statement(company)
    CF = yf.get_cash_flow(company)
    Y = BS.columns

# Get the data for a single company:
def data(ticker):
    global balance_sheet
    global income_statement
    global cfs
    global years
    balance_sheet = yf.get_balance_sheet(ticker)
    income_statement = yf.get_income_statement(ticker)
    cfs = yf.get_cash_flow(ticker)
    years = balance_sheet.columns    

# Compute PE RATIO:
def pe(ticker):
    global pe_ratio
    pe_ratio = yf.get_quote_table(ticker)['PE Ratio (TTM)']
    if pe_ratio != pe_ratio:
        pe_ratio = 0

# Compute PROFITABILITY:
def profitability():
    global profitability_score
    
    # SCORE 1 and SCORE 2: net income
    net_income = income_statement[years[0]]['netIncome']
    net_income_last = income_statement[years[1]]['netIncome']
    
    ni_score = 1 if net_income > 0 else 0
    ni_score_2 = 1 if net_income > net_income_last else 0
    
    # SCORE 3 - OPERATING CASH FLOW:
    op_cf = cfs[years[0]]['totalCashFromOperatingActivities']
    op_cf_score = 1 if op_cf > 0 else 0
    
    # SCORE 4 - Change in ROA
    avg_asset = (balance_sheet[years[0]]['totalAssets'] + 
                 balance_sheet[years[1]]['totalAssets'])/2
    avg_asset_last = (balance_sheet[years[1]]['totalAssets'] + 
                 balance_sheet[years[2]]['totalAssets'])/2
    ROA = net_income/avg_asset
    ROA_last = net_income_last/avg_asset_last
    ROA_score = 1 if ROA > ROA_last else 0
    
    # Score 5 - Accruals
    total_asset = balance_sheet[years[0]]['totalAssets']
    accruals = (op_cf/total_asset) - ROA
    accruals_score = 1 if accruals > 0 else 0
    
    # Compute the profitability score
    profitability_score = ni_score + ni_score_2 + op_cf_score + ROA_score + accruals_score
    
def leverage():
    global leverage_score  
    
    # SCORE 6 - long-term debt ratio:
    try:
        lt_debt = balance_sheet[years[0]]['longTermDebt']
        total_asset = balance_sheet[years[0]]['totalAssets']
        debt_ratio = lt_debt/total_asset
        debt_ratio_score = 1 if debt_ratio < 0.4 else 0
    except:
        debt_ratio_score = 1
    
    # SCORE 7 - Current ratio:
    current_asset = balance_sheet[years[0]]['totalCurrentAssets']
    current_liab = balance_sheet[years[0]]['totalCurrentLiabilities']
    current_ratio = current_asset/current_liab
    current_ratio_score = 1 if current_ratio > 1 else 0
    
    # Compute leverage score:
    leverage_score = debt_ratio_score + current_ratio_score

def operating_efficiency():
    global operating_efficiency_score
    
    # SCORE 8 - Gross Margin:
    gp = income_statement[years[0]]['grossProfit']
    gp_last = income_statement[years[1]]['grossProfit']
    revenue = income_statement[years[0]]['totalRevenue']
    revenue_last = income_statement[years[1]]['totalRevenue']
    
    gross_margin = gp/revenue
    gross_margin_last = gp_last/revenue_last 
    gross_margin_score = 1 if gross_margin > gross_margin_last else 0
    
    # SCORE 9 - Asset Turnover:
    avg_asset = (balance_sheet[years[0]]['totalAssets'] + 
                     balance_sheet[years[1]]['totalAssets'])/2
    avg_asset_last = (balance_sheet[years[1]]['totalAssets'] + 
                     balance_sheet[years[2]]['totalAssets'])/2
    asset_turnover = revenue/avg_asset
    asset_turnover_last = revenue_last/avg_asset_last
    asset_turnover_score = 1 if asset_turnover > asset_turnover_last else 0
    
    # Compute operating efficiency score:
    operating_efficiency_score = gross_margin_score + asset_turnover_score
    
# looping for all the selected tickers:

tick_range_1 = int(input('Give me a starting point : '))
tick_range_2 = int(input('Give me a ending point : '))

    
for ticker in tickers[tick_range_1:tick_range_2]:
    try:
        data(ticker)
        pe(ticker)
        profitability()
        leverage()
        operating_efficiency()
        
        new_row = {'TICKER':ticker,
                   'PE RATIO':pe_ratio,
                   'PROFITABILITY': profitability_score,
                   'LEVERAGE': leverage_score,
                   'OPERATING EFFICIENCY': operating_efficiency_score}
        
        summary = summary.append(new_row, ignore_index = True)
    
        print( ticker + ' - added')
        time.sleep(3)
        
    except:
        print(ticker + 'Something went wrong...')
        
summary['TOTAL SCORE'] = summary['PROFITABILITY'] + summary['LEVERAGE'] + summary['OPERATING EFFICIENCY']
print('---------------------------------------------------')
print(summary)
#summary.to_csv('Piotrosky_score.csv')

analysis = input('Do you want to specifically analyse one company? : ')
if analysis == 'yes':
    company = input('Insert the ticker for the selected company : ') 
    company_data(company)
    print('- Press BS for Balance Sheet\
                                - Press I for Income Statement\
                       - Press CF for Cash Flow Statement\
                          - Press ALL for all the documents')
           
    document = input('Which document do you want? ')
                     
    if document == 'BS': 
        print(BS)
    elif document == 'I':
        print(I)
    elif document == 'CF':
        print(CF)
    elif document == 'ALL':
         print(BS)
         print(I)
         print(CF)
    else:
        print('I suggest you to run again the program')
else:
    print('Thank you, bye!')
    