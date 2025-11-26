# File: svcj_engine/svcj_wrapper.pyx

# distutils: language = c
# distutils: sources = svcjmath.c
import numpy as np
import pandas as pd
cimport numpy as np

cdef extern from "svcjmath.h":
    int svcj_full_rolling_fit_2d(const double*, int, int, int, int, double*)
    int NUM_PARAMS

def generate_svcj_factor_matrix(
    log_returns_df: pd.DataFrame,
    int window_size, 
    int step_size
):
    """
    High-performance SVCJ factor generation engine.

    Accepts a pandas DataFrame of log returns, runs the C core, and returns
    a fully formatted pandas DataFrame containing the time-series of risk factors.

    Args:
        log_returns_df (pd.DataFrame): DataFrame with dates as index and assets
            as columns, containing log returns.
        window_size (int): The rolling window size in days.
        step_size (int): The step size for the rolling window in days.

    Returns:
        pd.DataFrame: A T x (A x F) DataFrame containing the time-series of
            the 8 estimated SVCJ factors for each asset.
    """
    cdef np.ndarray[np.float64_t, ndim=2] returns_matrix = log_returns_df.values
    asset_names = log_returns_df.columns.tolist()
    
    cdef int total_T = returns_matrix.shape[0]
    cdef int total_A = returns_matrix.shape[1]
    cdef int max_rolls = (total_T - window_size) // step_size + 1
    
    cdef np.ndarray[np.float64_t, ndim=1] output_buffer = np.zeros(max_rolls * total_A * NUM_PARAMS, dtype=np.float64)
    
    cdef int actual_rolls = svcj_full_rolling_fit_2d(
        &returns_matrix[0, 0], 
        total_T, total_A, window_size, step_size, &output_buffer[0]
    )
    
    cdef np.ndarray[np.float64_t, ndim=3] drift_tensor_3d = \
        output_buffer[:actual_rolls * total_A * NUM_PARAMS].reshape(actual_rolls, total_A, NUM_PARAMS)
    
    cdef np.ndarray[np.float64_t, ndim=3] transposed_tensor = np.transpose(drift_tensor_3d, (0, 1, 2))
    
    cdef np.ndarray[np.float64_t, ndim=2] final_matrix_2d = transposed_tensor.reshape(actual_rolls, -1)
    
    param_names = ['mu', 'kappa', 'theta', 'sigma_v', 'rho', 'lambda', 'mu_J', 'sigma_J']
    final_columns = [f'{asset}_{factor}' for asset in asset_names for factor in param_names]
    
    index_end_points = np.arange(window_size - 1, window_size - 1 + actual_rolls * step_size, step_size)
    final_index = log_returns_df.index[index_end_points]
    
    return pd.DataFrame(final_matrix_2d, index=final_index, columns=final_columns)