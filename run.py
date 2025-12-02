
!pip install git+https://github.com/N2304862K/SVCJ_Factor_Engine.git
# --- Block 1: Compilation ---
import numpy as np
import pandas as pd
import yfinance as yf
from typing import Dict, List
from svcj_wrapper import generate_svcj_factor_matrix

# This is the final, clean function the user interacts with
def generate_svcj_factors(
    tickers: List[str],
    start_date: str,
    end_date: str,
    window_size: int,
    step_size: int
) -> pd.DataFrame:
    print(f"\n1. Downloading and Preprocessing Data for {len(tickers)} tickers...")

    data = yf.download(tickers, start=start_date, end=end_date, progress=False, auto_adjust=True)['Close']
    if isinstance(data, pd.Series): data = data.to_frame(tickers[0])
    # The one unavoidable preprocessing step
    log_returns_df = np.log(data / data.shift(1)).dropna(how='all').fillna(0)

    print(f"2. Executing single call to the High-Speed Cython/C Core...")

    # --- THIS IS THE SINGLE, SIMPLIFIED, DATAFRAME-IN/DATAFRAME-OUT CALL ---
    final_factor_df = generate_svcj_factor_matrix(log_returns_df, window_size, step_size)

    print("3. C Core Finished. Final DataFrame is ready.")
    return final_factor_df

if __name__ == '__main__':
    # --- User Interaction is now the simplest possible ---
    TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JPM', 'V', 'PYPL', 'NFLX', 'WMT']

    # The user only provides the raw inputs to the high-level function
    final_factor_matrix = generate_svcj_factors(
        tickers=TICKERS,
        start_date='2020-01-01',
        end_date='2023-12-31',
        window_size=126,
        step_size=1
    )

    print("\n--- Final Factor Matrix (DataFrame I/O Interface) ---")

    sample_cols = ['AAPL_sigma_v', 'AAPL_lambda', 'AAPL_kappa', 'TSLA_sigma_v', 'TSLA_lambda', 'TSLA_kappa']

    print(f"Matrix Shape (Time Steps x Total Features): {final_factor_matrix.shape}")
    print("\nVerification of Financially Sensible Factor Drift:")
    print(final_factor_matrix[sample_cols].tail(5).to_string())
