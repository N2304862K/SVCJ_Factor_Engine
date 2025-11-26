# distutils: language = c
# distutils: sources = svcjmath.c
import numpy as np
import pandas as pd
cimport numpy as np

cdef extern from "svcjmath.h":
    int svcj_full_rolling_fit_2d(const double*, int, int, int, int, double*)
    int NUM_PARAMS

def generate_svcj_factor_matrix(object log_returns_df, int window_size, int step_size):
    """
    Accepts a pandas DataFrame (T x A), runs the C core, 
    and returns a fully formatted pandas DataFrame (T x (A*F)).
    """
    # 1. Prepare Inputs
    cdef np.ndarray[np.float64_t, ndim=2] returns_matrix = log_returns_df.values.astype(np.float64)
    asset_names = log_returns_df.columns.tolist()
    
    cdef int total_T = returns_matrix.shape[0]
    cdef int total_A = returns_matrix.shape[1]
    cdef int max_rolls = (total_T - window_size) // step_size + 1
    
    # 2. Allocate Output Buffer
    cdef np.ndarray[np.float64_t, ndim=1] output_buffer = np.zeros(max_rolls * total_A * NUM_PARAMS, dtype=np.float64)
    
    # 3. Run C Core
    cdef int actual_rolls = svcj_full_rolling_fit_2d(
        &returns_matrix[0, 0], 
        total_T, total_A, window_size, step_size, &output_buffer[0]
    )
    
    # 4. Reshape and Format Output
    # The C core fills data in [Roll, Asset, Param] order (linear memory)
    # Reshape to 3D: (Rolls, Assets, Params)
    cdef np.ndarray[np.float64_t, ndim=3] drift_tensor = \
        output_buffer[:actual_rolls * total_A * NUM_PARAMS].reshape(actual_rolls, total_A, NUM_PARAMS)
    
    # Flatten to 2D: (Rolls, Assets * Params)
    cdef np.ndarray[np.float64_t, ndim=2] final_matrix_2d = drift_tensor.reshape(actual_rolls, -1)
    
    # Construct Column Labels
    param_names = ['mu', 'kappa', 'theta', 'sigma_v', 'rho', 'lambda', 'mu_J', 'sigma_J']
    final_columns = [f'{asset}_{factor}' for asset in asset_names for factor in param_names]
    
    # Construct Index
    index_end_points = np.arange(window_size - 1, window_size - 1 + actual_rolls * step_size, step_size)
    final_index = log_returns_df.index[index_end_points]
    
    return pd.DataFrame(final_matrix_2d, index=final_index, columns=final_columns)