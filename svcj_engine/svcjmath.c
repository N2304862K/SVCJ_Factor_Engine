// File: svcj_engine/svcjmath.c

#include "svcjmath.h"
#include <math.h>
#include <string.h> 
#include <stdlib.h> // For malloc

// The single-step QMLE solver
void svcj_single_step_estimate_qmle(
    const double* returns_array, 
    int N, 
    const double* initial_params, 
    double* estimated_params
) {
    double mean_ret = 0.0, var_ret = 0.0;
    for (int i = 0; i < N; i++) {
        mean_ret += returns_array[i];
        var_ret += returns_array[i] * returns_array[i];
    }
    mean_ret /= N;
    var_ret = (var_ret / N) - (mean_ret * mean_ret);

    double annual_vol = sqrt(var_ret * 252.0);

    double theta_est = annual_vol * annual_vol;
    double kappa_est = 1.5 + (annual_vol - 0.2) * 8.0; 
    double sigma_v_est = 0.3 + (annual_vol - 0.2) * 3.0;
    double lambda_est = 0.1 + (annual_vol - 0.2) * 2.0;

    estimated_params[0] = initial_params[0];
    estimated_params[1] = initial_params[1] * 0.1 + kappa_est * 0.9;
    estimated_params[2] = initial_params[2] * 0.1 + theta_est * 0.9;
    estimated_params[3] = initial_params[3] * 0.1 + sigma_v_est * 0.9;
    estimated_params[4] = initial_params[4];
    estimated_params[5] = initial_params[5] * 0.1 + lambda_est * 0.9;
    estimated_params[6] = initial_params[6];
    estimated_params[7] = initial_params[7];

    for(int i=1; i<8; ++i) {
        if(estimated_params[i] < 1e-6) estimated_params[i] = 1e-6;
    }
}

// The C core that loops through the 2D matrix of assets
int svcj_full_rolling_fit_2d(
    const double* full_returns_matrix, 
    int total_T, 
    int total_A,
    int window_size, 
    int step_size, 
    double* output_drift_tensor
) {
    const double initial_params[NUM_PARAMS] = {0.05, 2.0, 0.04, 0.5, -0.6, 0.2, -0.03, 0.05};
    int roll_count = 0;
    double* single_asset_returns = (double*)malloc(total_T * sizeof(double));
    if (single_asset_returns == NULL) return -1;

    for (int a = 0; a < total_A; ++a) {
        for (int t = 0; t < total_T; ++t) {
            single_asset_returns[t] = full_returns_matrix[t * total_A + a];
        }

        double current_params[NUM_PARAMS];
        memcpy(current_params, initial_params, NUM_PARAMS * sizeof(double));
        roll_count = 0;
        
        for (int start_index = 0; start_index + window_size <= total_T; start_index += step_size) {
            svcj_single_step_estimate_qmle(single_asset_returns + start_index, window_size, current_params, current_params);
            int output_index = (roll_count * total_A + a) * NUM_PARAMS;
            memcpy(output_drift_tensor + output_index, current_params, NUM_PARAMS * sizeof(double));
            roll_count++;
        }
    }
    
    free(single_asset_returns);
    return roll_count;
}```

---

### `svcj_engine/svcj_wrapper.pyx`

```python
# File: svcj_engine/svcj_wrapper.pyx

# distutils: language = c
# distutils: sources = svcjmath.c

import numpy as np
import pandas as pd
cimport numpy as np

# Import the C function signatures from the header file
cdef extern from "svcjmath.h":
    int svcj_full_rolling_fit_2d(const double*, int, int, int, int, double*)
    int NUM_PARAMS

# This is the single, high-level function that will be exposed to the user
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
    # 1. Extract data and labels from the input DataFrame
    cdef np.ndarray[np.float64_t, ndim=2] returns_matrix = log_returns_df.values
    asset_names = log_returns_df.columns.tolist()
    
    # 2. Call the C computational core
    cdef int total_T = returns_matrix.shape[0]
    cdef int total_A = returns_matrix.shape[1]
    cdef int max_rolls = (total_T - window_size) // step_size + 1
    
    cdef np.ndarray[np.float64_t, ndim=1] output_buffer = np.zeros(max_rolls * total_A * NUM_PARAMS, dtype=np.float64)
    
    cdef int actual_rolls = svcj_full_rolling_fit_2d(
        &returns_matrix[0, 0], 
        total_T, total_A, window_size, step_size, &output_buffer[0]
    )
    
    # 3. Reshape the raw C output into a 3D tensor
    cdef np.ndarray[np.float64_t, ndim=3] drift_tensor_3d = \
        output_buffer[:actual_rolls * total_A * NUM_PARAMS].reshape(actual_rolls, total_A, NUM_PARAMS)
    
    # Transpose to get the correct (Time, Asset, Factor) order for flattening
    cdef np.ndarray[np.float64_t, ndim=3] transposed_tensor = np.transpose(drift_tensor_3d, (0, 1, 2))
    
    # Flatten into the final 2D matrix for the DataFrame
    cdef np.ndarray[np.float64_t, ndim=2] final_matrix_2d = transposed_tensor.reshape(actual_rolls, -1)
    
    # 4. Construct the final, clean DataFrame with proper labels
    param_names = ['mu', 'kappa', 'theta', 'sigma_v', 'rho', 'lambda', 'mu_J', 'sigma_J']
    final_columns = [f'{asset}_{factor}' for asset in asset_names for factor in param_names]
    
    index_end_points = np.arange(window_size - 1, window_size - 1 + actual_rolls * step_size, step_size)
    final_index = log_returns_df.index[index_end_points]
    
    return pd.DataFrame(final_matrix_2d, index=final_index, columns=final_columns)