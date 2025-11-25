# svcj_fast_factors/svcj_wrapper.pyx
# distutils: language = c
# distutils: sources = src/svcjmath.c

import numpy as np
import pandas as pd
cimport numpy as np

# Declare the C function signature from the header
cdef extern from "src/svcjmath.h":
    int svcj_full_rolling_fit_2d(const double* full_returns_matrix, int total_T, int total_A, int window_size, int step_size, double* output_drift_tensor)
    int NUM_PARAMS

# This is the final, high-level Python function exposed to the user
def generate_svcj_factor_matrix(
    log_returns_df: pd.DataFrame,
    int window_size, 
    int step_size
) -> pd.DataFrame:
    """
    Accepts a pandas DataFrame, runs the C core, and returns a fully
    formatted pandas DataFrame. All low-level details are hidden here.
    """
    # --- 1. Extract raw data and labels from the input DataFrame ---
    # Cython efficiently gets the raw NumPy array and its dimensions
    cdef np.ndarray[np.float64_t, ndim=2] returns_matrix = log_returns_df.values
    asset_names = log_returns_df.columns.tolist()
    
    # --- 2. Call the C computational core ---
    cdef int total_T = returns_matrix.shape[0]
    cdef int total_A = returns_matrix.shape[1]
    
    # Pre-allocate memory for the 3D output tensor (flattened)
    cdef int max_rolls = (total_T - window_size) // step_size + 1
    cdef np.ndarray[np.float64_t, ndim=1] output_buffer = np.zeros(max_rolls * total_A * NUM_PARAMS, dtype=np.float64)
    
    # Call the C core function
    cdef int actual_rolls = svcj_full_rolling_fit_2d(
        &returns_matrix[0, 0], 
        total_T, total_A, window_size, step_size, &output_buffer[0]
    )
    
    # --- 3. Perform all output formatting internally ---
    # Reshape the raw C output into a 3D tensor (Time x Asset x Factor)
    cdef np.ndarray[np.float64_t, ndim=3] drift_tensor_3d = \
        output_buffer[:actual_rolls * total_A * NUM_PARAMS].reshape(actual_rolls, total_A, NUM_PARAMS)
    
    # Flatten the (Asset, Factor) dimensions into a single column block for the DataFrame
    cdef np.ndarray[np.float64_t, ndim=2] final_matrix_2d = drift_tensor_3d.reshape(actual_rolls, -1)
    
    # Construct the final, clean DataFrame
    param_names = ['mu', 'kappa', 'theta', 'sigma_v', 'rho', 'lambda', 'mu_J', 'sigma_J']
    final_columns = [f'{asset}_{factor}' for asset in asset_names for factor in param_names]
    
    # Correctly determine the DataFrame index (time labels)
    index_end_points = np.arange(window_size - 1, window_size - 1 + actual_rolls * step_size, step_size)
    final_index = log_returns_df.index[index_end_points]
    
    return pd.DataFrame(final_matrix_2d, index=final_index, columns=final_columns)
