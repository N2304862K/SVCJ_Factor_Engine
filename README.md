# SVCJ Factor Engine

A high-speed, pre-compiled engine for generating time-varying SVCJ (Stochastic Volatility with Correlated Jumps) risk factors from financial time series data.

This package is designed for large-scale quantitative analysis and factor discovery, where a robust and financially sensible set of stationary features is required for downstream machine learning models. The core computational engine is written in C and wrapped with Cython for maximum performance, while the interface is a simple, user-friendly Python function that works directly with pandas DataFrames.

## Key Features

-   **High-Speed:** The core rolling-window estimation loop is executed in pre-compiled C, making it suitable for large asset universes and long time horizons.
-   **DataFrame I/O:** The engine accepts a standard pandas DataFrame of log returns and returns a fully formatted DataFrame of factors, abstracting away all complex C/NumPy conversions.
-   **Financially Sound:** Uses a robust QMLE (Quasi-Maximum Likelihood Estimation) methodology to ensure that the generated factors (e.g., volatility of volatility, jump intensity) are financially sensible and asset-relative.
-   **Modern Packaging:** Built using `pyproject.toml` (PEP 517/518) for reliable and robust remote installation.

## Installation

You can install the package directly from the GitHub repository using `pip`. The build process requires a C compiler (available by default in most Linux/macOS environments and Colab).

```bash
pip install git+https://github.com/N2304862K/SVCJ_Factor_Engine.git
```

## Usage

The package exposes a single, high-level function: `generate_svcj_factor_matrix`. The user provides a DataFrame of log returns, and the function returns the complete factor matrix.

```python
import pandas as pd
import numpy as np
from svcj_engine import generate_svcj_factor_matrix

# 1. Prepare your input data
# The input must be a pandas DataFrame where:
# - The index is a DatetimeIndex.
# - The columns are your asset tickers.
# - The values are the daily log returns.

# Example: Create a mock DataFrame of log returns for 3 assets
dates = pd.date_range(start='2020-01-01', periods=500, freq='D')
asset_data = {
    'ASSET_A': np.random.normal(0.0001, 0.01, 500),
    'ASSET_B': np.random.normal(0.0002, 0.02, 500),
    'ASSET_C': np.random.normal(0.0003, 0.03, 500),
}
log_returns_df = pd.DataFrame(asset_data, index=dates)

# 2. Define the rolling window parameters
window = 126  # 6-month rolling window
step = 5      # 1-week (5 trading days) step size

# 3. Generate the factor matrix with a single function call
# The C core handles all the complex looping and estimation internally.
factor_matrix = generate_svcj_factor_matrix(
    log_returns_df=log_returns_df,
    window_size=window,
    step_size=step
)

# 4. Analyze the output
# The output is a T x (A x F) DataFrame, ready for ML models.
print("--- Final Factor Matrix ---")
print(f"Shape: {factor_matrix.shape}")
print("\nSample of generated factors for ASSET_A and ASSET_B:")

# Display key risk factors for comparison
print(factor_matrix[['ASSET_A_sigma_v', 'ASSET_A_lambda', 'ASSET_B_sigma_v', 'ASSET_B_lambda']].tail())
```

## Output Factors

The engine generates 8 distinct SVCJ risk factors for each asset at each time step. The output DataFrame columns are named using the convention `{asset_name}_{factor_name}`.

The 8 factors are:
-   `mu`: The long-term drift of the asset.
-   `kappa`: The mean-reversion speed of volatility. A high value means volatility shocks dissipate quickly.
-   `theta`: The long-term average variance.
-   `sigma_v`: The volatility of volatility (the "vertical risk component"). A high value indicates an unstable risk profile.
-   `rho`: The correlation between asset returns and volatility (the leverage effect).
-   `lambda`: The intensity of price jumps. A high value indicates frequent, large, unexpected price movements.
-   `mu_J`: The average size of the price jumps.
-   `sigma_J`: The volatility of the price jumps.
```