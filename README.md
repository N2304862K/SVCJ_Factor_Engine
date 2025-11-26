# SVCJ Factor Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance, C/Cython-accelerated engine for generating stationary, asset-relative SVCJ (Stochastic Volatility with Correlated Jumps) risk factors from a time-series of financial returns.

This tool is designed for large-scale factor discovery processes in quantitative finance, where speed and robust, financially sensible outputs are critical.

## Key Features

- **High-Speed Core:** The entire rolling computation loop is executed in pre-compiled C, offering maximum performance.
- **DataFrame I/O:** The interface is strictly limited to a "DataFrame-in, DataFrame-out" design for ease of use.
- **Robust Estimation:** Uses a high-speed QMLE (Quasi-Maximum Likelihood Estimation) heuristic to provide financially sensible, non-constant, and `NaN`-free parameter drifts.
- **Stationary Features:** Transforms raw, non-stationary return series into a set of 8 stationary risk factors, ideal for downstream machine learning models.

## Installation

This package contains a C extension and must be compiled from source. The modern `pyproject.toml` setup handles all dependencies (like Cython and NumPy) automatically.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/N2304862K/SVCJ_Factor_Engine.git
    cd SVCJ_Factor_Engine
    ```

2.  **Install the package:**
    `pip` will automatically read `pyproject.toml`, install the build dependencies, and then compile and install the engine.
    ```bash
    pip install .
    ```

## Usage

The engine exposes a single, high-level function `generate_factors`. It takes a pandas DataFrame of log returns and returns a formatted DataFrame of SVCJ factors.

```python
import pandas as pd
import numpy as np
from svcj_engine import generate_factors # Import the main function

# 1. Prepare your input DataFrame
# The input must be a DataFrame where:
# - The index is a DatetimeIndex.
# - Each column represents an asset.
# - The values are the daily log returns.

# Example with mock data:
dates = pd.date_range(start='2020-01-01', periods=500, freq='D')
asset_data = {
    'LOW_VOL_ASSET': np.random.normal(0.0001, 0.01, 500),
    'HIGH_VOL_ASSET': np.random.normal(0.0002, 0.03, 500) + 
                     np.random.choice(, 500, p=[0.95, 0.05]) * -0.1
}
log_returns_df = pd.DataFrame(asset_data, index=dates)


# 2. Generate the SVCJ factor matrix
# The user only needs to provide the DataFrame, window size, and step size.
factor_matrix = generate_factors(
    log_returns_df=log_returns_df,
    window_size=126,  # e.g., 6-month window
    step_size=5       # e.g., weekly roll
)

# 3. Analyze the output
print("--- Final Factor Matrix for ML Training ---")
print(f"Matrix Shape (Time Steps x Total Features): {factor_matrix.shape}")
print("\nVerification of Factor Drift:")
print(factor_matrix[['LOW_VOL_ASSET_sigma_v', 'LOW_VOL_ASSET_lambda', 'HIGH_VOL_ASSET_sigma_v', 'HIGH_VOL_ASSET_lambda']].tail())
'''

##  Reference
generate_factors(log_returns_df, window_size, step_size)
log_returns_df (pd.DataFrame): Input DataFrame of log returns (Time x Assets).
window_size (int): The lookback period for calculating the parameters.
step_size (int): The frequency of the rolling calculation (e.g., 1 for daily, 5 for weekly).
Returns (pd.DataFrame): A ready-to-use DataFrame of shape (Time_Steps x (Assets * 8 Factors)).