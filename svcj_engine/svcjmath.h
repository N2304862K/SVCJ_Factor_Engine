// svcj_fast_factors/src/svcjmath.h
#ifndef SVCJMATH_H
#define SVCJMATH_H

#define NUM_PARAMS 8

void svcj_single_step_estimate_qmle(
    const double* returns_array, 
    int N, 
    const double* initial_params, 
    double* estimated_params
);

int svcj_full_rolling_fit_2d(
    const double* full_returns_matrix,
    int total_T,
    int total_A,
    int window_size,
    int step_size,
    double* output_drift_tensor
);

#endif
