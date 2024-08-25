# Fundamental-Analysis
Fundamental Analysis of S&amp;P500 companies, performing an analysis of their financial statements. The purpose at the end is to compute a Piotroski Score of the different companies and the possibility to analyse the financial documents of the single companies.

In this repository are present two different files for this purpose, an old one and renewed one, built in the last months. The old one, called "Piotroski Score", simply show all the companies in the S&P500 and based one the number of the companies in the list is possible to compute the Piotroski Score, analysing its financial situation computing some KPIs. It's also possible, at the end of the code, to show a specific document of the financial statement from a specific company, allowing the user to analyse the document. However, apparently the API of the data provider, Yahoo Finance, is not working anymore. That's why it has been created a new file, called "Financial Statement Analysis", more brief and concise, in which the user can just insert the ticker of the company for performing the analysis of the financial statement of the selected firm and print the Piotroski Score, the different scores which form the overall Piotroski value, and a brief summary of useful financial information.
