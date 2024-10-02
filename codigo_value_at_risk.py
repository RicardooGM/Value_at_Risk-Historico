#Importando as bibliotecas

import pandas as pd 
import numpy as np 
import yfinance as yf 
import matplotlib.pyplot as plt
import datetime as dt

#Preço das ações

anos = 15
end_date = datetime.now()
startdate = end_date - dt.timedelta(days = 365 * anos)

tickers = ["SPY","BND","GLD","QQQ","VTI"]

preços = pd.DataFrame()

for ticker in tickers:
    dados = yf.download(ticker, startdate,end_date)
    preços[ticker] = dados["Adj Close"]

print(preços)

log_returns = np.log(preços/preços.shift(1))
log_returns = log_returns.dropna()

log_returns

portfolio_value = 1000000
pesos = np.array([1/len(tickers)]*len(tickers))
pesos

retorno_hist = (log_returns * pesos).sum(axis= 1 )
retorno_hist

dias = 5
range_return = retorno_hist.rolling(window= dias).sum()
range_return = range_return.dropna()
range_return

#Calculando o VaR

intervalo_confiança = 0.95

VaR = -np.percentile(range_return, 100 - (intervalo_confiança * 100))*portfolio_value
VaR

#Gráfico do VaR
return_window = dias
range_return = retorno_hist.rolling(window=return_window).sum()
range_return = range_return.dropna()

range_return_dollar = range_return * portfolio_value

plt.hist(range_return_dollar.dropna(), bins=50,density=True)
plt.xlabel(f'{return_window}-Day Portfolio Return(Dollar Value)')
plt.ylabel("Frequency")
plt.title(f'Distribution of Portfolio {return_window}-Day Returns(Dollar Value)')
plt.axvline(-VaR, color = "r", linestyle = "dashed", linewidth = 2, label=f'Var at {intervalo_confiança:.0%} confidence level')
plt.legend()
plt.show()