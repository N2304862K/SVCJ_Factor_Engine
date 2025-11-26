#include "svcjmath.h"
#include <math.h>
#include <string.h> 
#include <stdlib.h>

void svcj_single_step_estimate_qmle(
    const double* returns_array, int N, const double* initial_params, double* estimated_params
) {
    double mean_ret = 0.0, var_ret = 0.0;
    for (int i = 0; i < N; i++) {
        mean_ret += returns_array[i];
        var_ret += returns_array[i] * returns_array[i];
    }
    mean_ret /= N;
    var_ret = (var_ret / N) - (mean_ret * mean_ret);
    
    // Heuristics based on annualized volatility
    double annual_vol = sqrt(var_ret * 252.0);
    double theta_est = annual_vol * annual_vol;
    double kappa_est = 1.5 + (annual_vol - 0.2) * 8.0; 
    double sigma_v_est = 0.3 + (annual_vol - 0.2) * 3.0;
    double lambda_est = 0.1 + (annual_vol - 0.2) * 2.0;

    // Weighted update using initial_params for stability
    estimated_params[0] = initial_params[0];
    estimated_params[1] = initial_params[1] * 0.1 + kappa_est * 0.9;
    estimated_params[2] = initial_params[2] * 0.1 + theta_est * 0.9;
    estimated_params[3] = initial_params[3] * 0.1 + sigma_v_est * 0.9;
    estimated_params[4] = initial_params[4];
    estimated_params[5] = initial_params[5] * 0.1 + lambda_est * 0.9;
    estimated_params[6] = initial_params[6];
    estimated_params[7] = initial_params[7];

    for(int i=1; i<8; ++i) { if(estimated_params[i] < 1e-6) estimated_params[i] = 1e-6; }
}

int svcj_full_rolling_fit_2d(
    const double* full_returns_matrix, int total_T, int total_A,
    int window_size, int step_size, double* output_drift_tensor
) {
    const double initial_params[NUM_PARAMS] = {0.05, 2.0, 0.04, 0.5, -0.6, 0.2, -0.03, 0.05};
    double* single_asset_returns = (double*)malloc(total_T * sizeof(double));
    if (single_asset_returns == NULL) return -1;

    int roll_count = 0;
    for (int a = 0; a < total_A; ++a) {
        // Extract asset column
        for (int t = 0; t < total_T; ++t) {
            single_asset_returns[t] = full_returns_matrix[t * total_A + a];
        }

        double current_params[NUM_PARAMS];
        memcpy(current_params, initial_params, NUM_PARAMS * sizeof(double));
        roll_count = 0;
        
        for (int start_index = 0; start_index + window_size <= total_T; start_index += step_size) {
            svcj_single_step_estimate_qmle(single_asset_returns + start_index, window_size, current_params, current_params);
            
            // Store result in flat tensor buffer
            int output_index = (roll_count * total_A + a) * NUM_PARAMS;
            memcpy(output_drift_tensor + output_index, current_params, NUM_PARAMS * sizeof(double));
            roll_count++;
        }
    }
    
    free(single_asset_returns);
    return roll_count;
}