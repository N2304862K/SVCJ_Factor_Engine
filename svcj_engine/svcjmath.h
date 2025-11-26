// File: svcj_engine/svcjmath.h

#ifndef SVCJMATH_H
#define SVCJMATH_H

#define NUM_PARAMS 8

void svcj_single_step_estimate_qmle(const double*, int, const double*, double*);
int svcj_full_rolling_fit_2d(const double*, int, int, int, int, double*);

#endif