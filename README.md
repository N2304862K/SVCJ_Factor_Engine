```text
# File: README.txt

======================
 SVCJ Factor Engine
======================

A high-performance Python library, powered by C and Cython, designed for quantitative analysts and researchers to generate time-series of SVCJ (Stochastic Volatility with Correlated Jumps) risk factors.

This engine provides a simple, "DataFrame-in, DataFrame-out" interface, making it ideal for large-scale feature engineering in machine learning pipelines for factor discovery. The core logic is a robust, high-speed rolling Quasi-Maximum Likelihood Estimation (QMLE) model.


-------------------
 Features
-------------------

- **High-Speed Core:** The computational engine is written in C and wrapped with Cython for maximum performance, capable of processing large asset universes over long time horizons.
- **Simple Interface:** Abstracts away all complex C-level interactions. The user provides a pandas DataFrame of log returns and receives a fully formatted DataFrame of factors.
- **Rolling Window Analysis:** Generates a time-series of risk factors, not just a single-point estimate, which is essential for time-series ML models.
- **Robust Estimation:** Uses a QMLE-based model that provides financially sensible, asset-relative parameters, correctly distinguishing between low-volatility and high-volatility regimes.
- **ML-Ready Output:** The output is a single, flattened T x (A x F) DataFrame, where T is the number of time steps, A is the number of assets, and F is the number of factors. This format is ready for direct use as a feature matrix (X) in models like XGBoost, LSTMs, or Transformers.


-------------------
 Installation
-------------------

The package can be installed directly from the GitHub repository using pip. The C/Cython compilation will be handled automatically during the installation process.

Ensure you have a C compiler installed on your system. For most Linux distributions, this can be installed via `sudo apt-get install build-essential`. On macOS, install the Xcode command-line tools. On Windows, install Microsoft C++ Build Tools.

```
pip install git+https://github.com/N2304862K/SVCJ_Factor_Engine.git
```


-------------------
 Usage
-------------------

The engine requires a pandas DataFrame where the index is a DatetimeIndex and each column represents the log returns for a single asset.

Here is a complete example:

```python
import numpy as np
import pandas as pd
from svcj_engine import generate_svcj_factor_matrix

# 1. Prepare your input data
# The function requires a DataFrame of log returns.
# Index must be dates, columns must be asset tickers.
dates = pd.date_range(start='2020-01-01', periods=500, freq='D')
asset_data = {
    'STABLE_ASSET': np.random.normal(0.0001, 0.01, 500),
    'VOLATILE_ASSET': np.random.normal(0.0005, 0.03, 500) + 
                      np.random.choice(, size=500, p=[0.95, 0.05]) * 
                      np.random.normal(-0.05, 0.08, 500)
}
log_returns_df = pd.DataFrame(asset_data, index=dates)

# 2. Define the analysis parameters
window_size = 126  # 6-month rolling window
step_size = 5      # 1-week (5 trading days) step size

# 3. Generate the factor matrix with a single function call
# The C core handles all the complex looping and calculation.
factor_matrix = generate_svcj_factor_matrix(
    log_returns_df=log_returns_df,
    window_size=window_size,
    step_size=step_size
)

# 4. View the results
# The output is a clean, ML-ready DataFrame.
print("--- Final Factor Matrix for ML Training ---")
print(f"Matrix Shape (Time Steps x Total Features): {factor_matrix.shape}")
print("\nSample of Final Factor Matrix:")
print(factor_matrix.tail())
```


-----------------------------
 Output Factor Descriptions
-----------------------------

The engine generates 8 risk factors per asset for each time step. Key factors include:

- **sigma_v (Volatility of Volatility):** The "vertical risk" component. A high value indicates an unstable and unpredictable risk profile.
- **lambda (Jump Intensity):** The estimated frequency of large, discontinuous price movements (jumps).
- **kappa (Mean Reversion Rate):** The speed at which volatility shocks are expected to dissipate. A low value means risk is more persistent.
- **theta (Long-Term Volatility):** The long-run average level of the asset's variance.


-------------------
 License
-------------------

This project is licensed under the MIT License.```