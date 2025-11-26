# File: svcj_engine/__init__.py

# This file marks the 'svcj_engine' directory as a Python package.
# It also serves as the public API for the package, exposing the main
# user-facing function from the compiled Cython module.

# Import the high-level function from the compiled wrapper.
# This makes it accessible to the user via a simple import statement:
# from svcj_engine import generate_svcj_factor_matrix

from .svcj_wrapper import generate_svcj_factor_matrix

# Define what is exposed when a user does 'from svcj_engine import *'
__all__ = ['generate_svcj_factor_matrix']