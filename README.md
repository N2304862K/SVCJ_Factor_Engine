# High-Speed SVCJ Factor Engine

A high-performance, vectorized engine for generating **Stochastic Volatility with Correlated Jumps (SVCJ)** risk factors from historical asset returns.

Designed for large-scale **Factor Discovery** and **Financial Machine Learning** pipelines, this library wraps a pre-compiled C core with a clean Python/Pandas interface to deliver "DataFrame-in, DataFrame-out" functionality with zero Python loop overhead.

---

## 🚀 Key Features

*   **Black-Box Design:** No complex configuration. Pass a raw DataFrame of log returns; get back a clean DataFrame of stationary risk factors.
*   **C-Level Performance:** Core logic is implemented in C and optimized with Cython, handling multi-asset rolling windows in milliseconds.
*   **Stationary Features:** Converts non-stationary price data into 8 stationary, asset-relative parameters (e.g., `sigma_v`, `kappa`, `lambda`) ideal for ML inputs.
*   **Robust QMLE:** Uses a Quasi-Maximum Likelihood Estimation approach with robust heuristics to ensure financial stability (no `NaN`s or numerical explosions).

## 🛠️ Installation

This project requires a C compiler and the Python development headers.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Compile the Engine
Run the setup script to build the Cython wrapper and C core in place.
```bash
python setup.py build_ext --inplace
```

*Note: This generates a shared object file (`svcj_wrapper.so` or `.pyd`) in the directory, making the module importable.*

---

## ⚡ Quick Start

```python
import yfinance as yf
import numpy as np
import svcj_wrapper  # The compiled module

# 1. Get Data
tickers = ['AAPL', 'TSLA', 'MSFT', 'JPM']
data = yf.download(tickers, start='2020-01-01', end='2023-12-31')['Adj Close']
log_returns = np.log(data / data.shift(1)).dropna().fillna(0)

# 2. Generate Factors (Single Function Call)
# window_size=126 (6 months), step_size=5 (Weekly roll)
factor_df = svcj_wrapper.generate_svcj_factor_matrix(log_returns, 126, 5)

# 3. Output
# factor_df is a Time x (Assets * 8 Factors) DataFrame ready for ML
print(factor_df.head())
```

---

## 📊 Output Factors

For every asset provided, the engine generates 8 stationary risk factors:

| Factor | Name | Description | Role in ML |
| :--- | :--- | :--- | :--- |
| **`sigma_v`** | Volatility of Volatility | The "Vertical Risk." Measures the instability of the risk profile. | Regime change detection. |
| **`kappa`** | Mean Reversion | How quickly volatility shocks dissipate. | predicting shock duration. |
| **`theta`** | Long-Term Volatility | The baseline variance level. | Base risk anchor. |
| **`lambda`** | Jump Intensity | Frequency of sudden, discontinuous price moves. | Tail risk probability. |
| **`mu_J`** | Jump Mean | Average size/direction of jumps. | Directional tail risk. |
| **`rho`** | Correlation | Correlation between Returns and Volatility. | Leverage effect / skew. |
| **`mu`** | Drift | Constant drift component. | Trend bias. |
| **`sigma_J`** | Jump Volatility | Variance of the jump size distribution. | Tail fatness. |

## 📐 Architecture

The system follows a strict high-performance architecture:

1.  **Python Input:** Pandas DataFrame `(Time x Assets)`.
2.  **Cython Bridge:** Zero-copy transfer of NumPy memory buffers to C.
3.  **C Core:**
    *   Iterates through assets (Outer Loop).
    *   Performs rolling window slicing (Inner Loop).
    *   Executes Robust QMLE Solver (Heuristic Estimation).
4.  **Python Output:** Reshapes the flat C-tensor into a labeled Multi-Index DataFrame.

## ⚠️ Notes

*   **Heuristic Solver:** To ensure speed and stability for thousands of assets, the QMLE solver uses robust, data-driven heuristics rather than a full non-linear optimization (which is slow and prone to failure on noisy financial data).
*   **Data Prep:** Ensure your input DataFrame contains **Log Returns**, not prices. NaNs should be filled (e.g., with 0) before passing to the engine.

## 📄 License
MIT
