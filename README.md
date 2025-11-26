# SVCJ Factor Engine

A high-speed, pre-compiled engine for generating time-varying SVCJ (Stochastic Volatility with Correlated Jumps) risk factors from financial time series data.

This package is designed for large-scale quantitative analysis and factor discovery, where a robust and financially sensible set of stationary features is required for downstream machine learning models. The core computational engine is written in C and wrapped with Cython for maximum performance, while the interface is a simple, user-friendly Python function that works directly with pandas DataFrames.

## Key Features

-   **High-Speed:** The core rolling-window estimation loop is executed in pre-compiled C, making it suitable for large asset universes and long time horizons.
-   **DataFrame I/O:** The engine accepts a standard pandas DataFrame of log returns and returns a fully formatted DataFrame of factors, abstracting away all complex C/NumPy conversions.
-   **Financially Sound:** Uses a robust QMLE (Quasi-Maximum Likelihood Estimation) methodology to ensure that the generated factors (e.g., volatility of volatility, jump intensity) are financially sensible and asset-relative.
-   **No Dependencies:** The core engine has no external C dependencies and is built seamlessly during installation.

## Installation

You can install the package directly from the GitHub repository using `pip`. The build process requires a C compiler (available by default in most Linux/macOS environments and Colab).

```bash
pip install git+https://github.com/N2304862K/SVCJ_Factor_Engine.git