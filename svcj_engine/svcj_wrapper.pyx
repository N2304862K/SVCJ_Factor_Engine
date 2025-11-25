# distutils: language = c
# distutils: sources = svcjmath.c
import numpy as np
import pandas as pd
cimport numpy as np

cdef extern from "svcjmath.h":
    int svcj_full_rolling_fit_2d(const double*, int, int, int, int, double*)
    int NUM_PARAMS

# This is the final, high-level function exposed to the user
def generate_svcj_factor_matrix(
    log_returns_df: pd.DataFrame,
    int window_size, 
    int step_size
):
    """
    Accepts a pandas DataFrame, runs the C core, and returns a fully
    formatted pandas DataFrame. All ugly formatting is hidden here.
    """
    # --- 1. Extract data and labels from the input DataFrame ---
    cdef np.ndarray[np.float64_t, ndim=2] returns_matrix = log_returns_df.values
    asset_names = log_returns_df.columns.tolist()
    
    # --- 2. Call the C computational core ---
    cdef int total_T = returns_matrix.shape[0]
    cdef int total_A = returns_matrix.shape[1]
    cdef int max_rolls = (total_T - window_size) // step_size + 1
    
    cdef np.ndarray[np.float64_t, ndim=1] output_buffer = np.zeros(max_rolls * total_A * NUM_PARAMS, dtype=np.float64)
    
    cdef int actual_rolls = svcj_full_rolling_fit_2d(
        &returns_matrix[0, 0], 
        total_T, total_A, window_size, step_size, &output_buffer[0]
    )
    
    # --- 3. Perform all "ugly" formatting internally ---
    # Reshape the raw C output into a 3D tensor
    cdef np.ndarray[np.float64_t, ndim=3] drift_tensor_3d = \
        output_buffer[:actual_rolls * total_A * NUM_PARAMS].reshape(actual_rolls, total_A, NUM_PARAMS)
    
    # Transpose to get the correct (Time, Asset, Factor) order
    cdef np.ndarray[np.float64_t, ndim=3] transposed_tensor = np.transpose(drift_tensor_3d, (0, 1, 2))
    
    # Flatten into the final 2D matrix for the DataFrame
    cdef np.ndarray[np.float64_t, ndim=2] final_matrix_2d = transposed_tensor.reshape(actual_rolls, -1)
    
    # --- 4. Construct the final, clean DataFrame ---
    param_names = ['mu', 'kappa', 'theta', 'sigma_v', 'rho', 'lambda', 'mu_J', 'sigma_J']
    final_columns = [f'{asset}_{factor}' for asset in asset_names for factor in param_names]
    
    index_end_points = np.arange(window_size - 1, window_size - 1 + actual_rolls * step_size, step_size)
    final_index = log_returns_df.index[index_end_points]
    
    return pd.DataFrame(final_matrix_2d, index=final_index, columns=final_columns)
