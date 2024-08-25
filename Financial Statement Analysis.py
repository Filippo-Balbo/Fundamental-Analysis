#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 18:42:03 2024

@author: filippobalbo
"""

import pandas as pd
import numpy as np
import requests
import json 
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt

fmp_api_key = 'b2cf7eef57b0755e42416a78f8055651'
symbol = 'MSFT'
session = requests.Session()

BalanceSheet = []
IncomeStatement = []
CashFlow = []
years = []
QuoteStatement = []
StatementAnalysis = []

# GET DATA

Quote_url = f'https://financialmodelingprep.com/api/v3/quote/{symbol}?&apikey={fmp_api_key}'
response = requests.get(Quote_url) 
if response.status_code == 200: 
        dt4 = response.json()
        # Creating a DataFrame from the list of dictionaries
        QuoteStatement = pd.DataFrame(dt4)
        QuoteStatement = QuoteStatement.T

StatementAnalysis_url = f'https://financialmodelingprep.com/api/v3/key-metrics/{symbol}?period=annual&apikey={fmp_api_key}'
response = requests.get(StatementAnalysis_url) 
if response.status_code == 200: 
        dt0 = response.json()
        # Creating a DataFrame from the list of dictionaries
        StatementAnalysis = pd.DataFrame(dt0)
        StatementAnalysis = StatementAnalysis.T

Income_url = f'https://financialmodelingprep.com/api/v3/income-statement/{symbol}?period=annual&apikey={fmp_api_key}'
response = requests.get(Income_url) 
if response.status_code == 200: 
        dt1 = response.json()
        # Creating a DataFrame from the list of dictionaries
        IncomeStatement = pd.DataFrame(dt1)
        IncomeStatement = IncomeStatement.T

BalanceSheet_url = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?period=annual&apikey={fmp_api_key}'
response = requests.get(BalanceSheet_url)
if response.status_code == 200:
        dt2 = response.json()
        # Creating a DataFrame from the list of dictionaries
        BalanceSheet = pd.DataFrame(dt2)    
        BalanceSheet = BalanceSheet.T

CashFlow_url = f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{symbol}?period=annual&apikey={fmp_api_key}'
response = requests.get(CashFlow_url)
if response.status_code == 200:
        dt3 = response.json()
        # Creating a DataFrame from the list of dictionaries
        CashFlow = pd.DataFrame(dt3)   
        CashFlow = CashFlow.T
        
years = BalanceSheet.columns        
    

# PROFITABILITY SCORE
    
#Score #1 and #2 - net income
net_income = IncomeStatement[years[0]]['netIncome']
net_income_py = IncomeStatement[years[1]]['netIncome']
ni_score1 = 1 if net_income > 0 else 0
ni_score2 = 1 if net_income > net_income_py else 0

#Score 3 - Operating Cash Flow
op_cf = CashFlow[years[0]]['operatingCashFlow']
op_cf_score = 1 if op_cf > 0 else 0

#Score 4 - Change in ROA

avg_assets = (BalanceSheet[years[0]]['totalAssets'] + BalanceSheet[years[1]]['totalAssets'])/2
avg_assets_py = (BalanceSheet[years[1]]['totalAssets'] + BalanceSheet[years[2]]['totalAssets'])/2

RoA = net_income/avg_assets
RoA_py = net_income_py/avg_assets_py
RoA_score = 1 if RoA > RoA_py else 0

#Score 5 - Accruals
total_assets = BalanceSheet[years[0]]['totalAssets']
accruals = op_cf/total_assets - RoA
ac_score = 1 if accruals > 0 else 0

Profitability_Score = ni_score1 + ni_score2 + op_cf_score + RoA_score + ac_score



# LEVERAGE SCORE

# Score #6 - Long-Term Debt Ratio
lt_debt = BalanceSheet[years[0]]['longTermDebt']
debt_ratio = lt_debt/total_assets
debt_ratio_score = 1 if debt_ratio < 0.4 else 0 

# Score #7 - Current Ratio 
current_assets = BalanceSheet[years[0]]['totalCurrentAssets']
current_liab = BalanceSheet[years[0]]['totalCurrentLiabilities']
current_ratio = current_assets/current_liab
current_ratio_score = 1 if current_ratio > 1 else 0

Leverage_Score = debt_ratio_score + current_ratio_score


# OPERATING EFFICIENCY SCORE

# Score #8 - Gross Margin
gross_profit = IncomeStatement[years[0]]['grossProfit']
gross_profit_py = IncomeStatement[years[1]]['grossProfit']
revenue = IncomeStatement[years[0]]['revenue']
revenue_py = IncomeStatement[years[1]]['revenue']
gross_margin = gross_profit/revenue
gross_margin_py = gross_profit_py/revenue_py
gross_margin_score = 1 if gross_margin > gross_margin_py else 0

# # Score #9 - Asset Turnover
asset_turnover = revenue/avg_assets
asset_turnover_py = revenue_py/avg_assets_py
asset_turnover_score = 1 if asset_turnover > asset_turnover_py else 0

Operating_Efficiency_Score = gross_margin_score + asset_turnover_score # Indicate if the company is doing better than the year before, as seeling more than the year before with the asset they have in place


# Other Data:
pe_ratio = StatementAnalysis[years[0]]['peRatio']
total_score = Operating_Efficiency_Score + Leverage_Score + Profitability_Score
avg200_price = QuoteStatement[years[0]]['priceAvg200']
price = QuoteStatement[years[0]]['price']

# Summary:

Summary = pd.DataFrame(columns = ['Company Ticker','Price','Average 200 days price',
                       'PE Ratio','Profitability Score','Leverage Score',
                       'Operating Efficiency Score','Total Score'])        

row = {'Company Ticker' : symbol,
           'Price' : price,
           'Average 200 days price' : avg200_price,
           'PE Ratio' : pe_ratio,
           'Profitability Score' : Profitability_Score,
           'Leverage Score' : Leverage_Score,
           'Operating Efficiency Score' : Operating_Efficiency_Score,
           'Total Score': total_score}    
Summary = pd.concat([Summary, pd.DataFrame([row])], ignore_index = True)
Summary = Summary.T
print(Summary)


