// File: svcj_engine/svcjmath.h

#ifndef SVCJMATH_H
#define SVCJMATH_H

#define NUM_PARAMS 8

// Function signature for the single-window QMLE solver
void svcj_single_step_estimate_qmle(
    const double* returns_array, 
    int N, 
    const double* initial_params, 
    double* estimated_params
);

// Function signature for the high-speed C core that handles the 2D matrix
int svcj_full_rolling_fit_2d(
    const double* full_returns_matrix,
    int total_T,
    int total_A,
    int window_size,
    int step_size,
    double* output_drift_tensor
);

#endif