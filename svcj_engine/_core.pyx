# cython: language_level=3
import numpy as np
import pandas as pd
cimport numpy as np

# We tell Cython to expect these C functions. 
# "svcjmath.h" will be found because setup.py adds the folder to include_dirs.
cdef extern from "svcjmath.h":
    int svcj_full_rolling_fit_2d(const double*, int, int, int, int, double*)
    int NUM_PARAMS

def generate_svcj_factor_matrix(object log_returns_df, int window_size, int step_size):
    if not isinstance(log_returns_df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    # Ensure C-contiguous
    cdef np.ndarray[np.float64_t, ndim=2, mode="c"] returns_matrix = \
        np.ascontiguousarray(log_returns_df.values, dtype=np.float64)
    
    asset_names = log_returns_df.columns.tolist()
    cdef int total_T = returns_matrix.shape[0]
    cdef int total_A = returns_matrix.shape[1]
    
    if total_T < window_size:
        raise ValueError(f"Data length ({total_T}) < Window Size ({window_size})")

    cdef int max_rolls = (total_T - window_size) // step_size + 1
    cdef np.ndarray[np.float64_t, ndim=1] output_buffer = np.zeros(max_rolls * total_A * 8, dtype=np.float64)
    
    # Call C core
    cdef int actual_rolls = svcj_full_rolling_fit_2d(
        &returns_matrix[0, 0], 
        total_T, total_A, window_size, step_size, &output_buffer[0]
    )
    
    # Reshape and Format
    # 1. Reshape flat buffer to 3D Tensor (Rolls, Assets, Factors)
    cdef np.ndarray[np.float64_t, ndim=3] drift_tensor = \
        output_buffer[:actual_rolls * total_A * 8].reshape(actual_rolls, total_A, 8)
    
    # 2. Transpose to (Rolls, Assets, Factors) - Already in correct shape from C loop?
    # C loop fills: Roll 0 (Asset 0, Asset 1...), Roll 1...
    # So drift_tensor[r, a, f] is correct.
    
    # 3. Flatten to 2D (Rolls, Assets*Factors)
    cdef np.ndarray[np.float64_t, ndim=2] final_matrix = drift_tensor.reshape(actual_rolls, -1)
    
    # 4. Create DataFrame
    param_names = ['mu', 'kappa', 'theta', 'sigma_v', 'rho', 'lambda', 'mu_J', 'sigma_J']
    cols = [f'{a}_{p}' for a in asset_names for p in param_names]
    idx = log_returns_df.index[window_size - 1 : window_size - 1 + actual_rolls * step_size : step_size]
    
    return pd.DataFrame(final_matrix, index=idx, columns=cols)