import numpy as np
import pandas as pd
import yfinance as yf
import svcj_wrapper # This import works after compilation

def run_pipeline():
    tickers = ['AAPL', 'TSLA', 'MSFT']
    print(f"Downloading data for: {tickers}")
    
    # Data Prep
    data = yf.download(tickers, start='2022-01-01', end='2023-12-31', progress=False)['Adj Close']
    log_returns = np.log(data / data.shift(1)).dropna(how='all').fillna(0)
    
    print("Running SVCJ Engine...")
    # Single call DataFrame In -> DataFrame Out
    factors = svcj_wrapper.generate_svcj_factor_matrix(log_returns, window_size=126, step_size=5)
    
    print(f"Done. Output Shape: {factors.shape}")
    print(factors[['AAPL_sigma_v', 'TSLA_sigma_v']].tail())

if __name__ == "__main__":
    run_pipeline()