# distutils: language = c
# distutils: sources = src/svcj_estimator/svcjmath.c
import numpy as np
import pandas as pd
cimport numpy as np

cdef extern from "svcjmath.h":
    int svcj_full_rolling_fit_2d(const double*, int, int, int, int, double*)
    int NUM_PARAMS

def generate_svcj_factor_matrix(
    object log_returns_df,  # Accepts pandas DataFrame
    int window_size, 
    int step_size
):
    """
    Core driver: DataFrame In -> C-Computation -> DataFrame Out.
    """
    # Type check to ensure it's a pandas DataFrame
    if not isinstance(log_returns_df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    # --- 1. Prepare Data ---
    # Force C-contiguous array of doubles
    cdef np.ndarray[np.float64_t, ndim=2, mode="c"] returns_matrix = \
        np.ascontiguousarray(log_returns_df.values, dtype=np.float64)
    
    asset_names = log_returns_df.columns.tolist()
    
    # --- 2. Call C Core ---
    cdef int total_T = returns_matrix.shape[0]
    cdef int total_A = returns_matrix.shape[1]
    cdef int max_rolls = (total_T - window_size) // step_size + 1
    
    if max_rolls <= 0:
        raise ValueError(f"Data length ({total_T}) is smaller than window size ({window_size})")

    cdef np.ndarray[np.float64_t, ndim=1] output_buffer = np.zeros(max_rolls * total_A * NUM_PARAMS, dtype=np.float64)
    
    cdef int actual_rolls = svcj_full_rolling_fit_2d(
        &returns_matrix[0, 0], 
        total_T, total_A, window_size, step_size, &output_buffer[0]
    )
    
    # --- 3. Format Output ---
    cdef np.ndarray[np.float64_t, ndim=3] drift_tensor_3d = \
        output_buffer[:actual_rolls * total_A * NUM_PARAMS].reshape(actual_rolls, total_A, NUM_PARAMS)
    
    # Transpose to (Time, Asset, Factor)
    cdef np.ndarray[np.float64_t, ndim=3] transposed_tensor = np.transpose(drift_tensor_3d, (0, 1, 2))
    
    # Flatten to 2D (Time, Asset*Factor)
    cdef np.ndarray[np.float64_t, ndim=2] final_matrix_2d = transposed_tensor.reshape(actual_rolls, -1)
    
    # Construct DataFrame
    param_names = ['mu', 'kappa', 'theta', 'sigma_v', 'rho', 'lambda', 'mu_J', 'sigma_J']
    final_columns = [f'{asset}_{factor}' for asset in asset_names for factor in param_names]
    
    index_end_points = np.arange(window_size - 1, window_size - 1 + actual_rolls * step_size, step_size)
    final_index = log_returns_df.index[index_end_points]
    
    return pd.DataFrame(final_matrix_2d, index=final_index, columns=final_columns)