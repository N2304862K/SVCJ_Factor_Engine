// svcj_fast_factors/src/svcjmath.c
#include "svcjmath.h"
#include <math.h>
#include <string.h> 
#include <stdlib.h> 

// This simulates a fast-converging QMLE solver for a single window.
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

    // Use a weighted average with the previous step's estimate for stability
    estimated_params[0] = initial_params[0]; // mu is less volatile, fixed here
    estimated_params[1] = initial_params[1] * 0.1 + kappa_est * 0.9;
    estimated_params[2] = initial_params[2] * 0.1 + theta_est * 0.9;
    estimated_params[3] = initial_params[3] * 0.1 + sigma_v_est * 0.9;
    estimated_params[4] = initial_params[4]; // rho is fixed
    estimated_params[5] = initial_params[5] * 0.1 + lambda_est * 0.9;
    estimated_params[6] = initial_params[6]; // mu_J is fixed
    estimated_params[7] = initial_params[7]; // sigma_J is fixed

    // Enforce physical constraints
    for(int i=1; i<8; ++i) { // mu is 0
        if(estimated_params[i] < 1e-6) estimated_params[i] = 1e-6;
    }
}

// This C function contains the asset-by-asset loop and calls the single-step solver.
int svcj_full_rolling_fit_2d(
    const double* full_returns_matrix, int total_T, int total_A,
    int window_size, int step_size, double* output_drift_tensor
) {
    // --- Internal Initialization of fixed parameters for the solver ---
    const double initial_params_for_solver[NUM_PARAMS] = {0.05, 2.0, 0.04, 0.5, -0.6, 0.2, -0.03, 0.05};
    // --- End of Internal Initialization ---

    double* single_asset_returns = (double*)malloc(total_T * sizeof(double));
    if (single_asset_returns == NULL) return -1; // Memory allocation error

    // Outer loop: Iterate through each asset (column)
    for (int a = 0; a < total_A; ++a) {
        // Extract the full time series for the current asset (col-major to row-major)
        for (int t = 0; t < total_T; ++t) {
            single_asset_returns[t] = full_returns_matrix[t * total_A + a];
        }

        double current_params_for_asset[NUM_PARAMS];
        memcpy(current_params_for_asset, initial_params_for_solver, NUM_PARAMS * sizeof(double));
        
        // Inner loop: The rolling window for the current asset
        int roll_count_per_asset = 0;
        for (int start_index = 0; start_index + window_size <= total_T; start_index += step_size) {
            svcj_single_step_estimate_qmle(
                single_asset_returns + start_index, 
                window_size, 
                current_params_for_asset, 
                current_params_for_asset
            );
            // Place the result into the correct 3D tensor slot (Time x Asset x Factor)
            int output_index = (roll_count_per_asset * total_A + a) * NUM_PARAMS;
            memcpy(output_drift_tensor + output_index, current_params_for_asset, NUM_PARAMS * sizeof(double));
            roll_count_per_asset++;
        }
    }
    
    free(single_asset_returns);
    // Return the number of rolls for a single asset (assumed consistent across all assets)
    return (total_T - window_size) / step_size + 1; 
}
