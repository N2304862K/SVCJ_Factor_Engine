# setup.py
import os
import numpy
from setuptools import setup, Extension
from Cython.Build import cythonize

# 1. Define the path to the local source directory
# This ensures the C compiler finds "svcjmath.h"
current_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.join(current_dir, "svcj_engine")

# 2. Define the Extension
extensions = [
    Extension(
        name="svcj_engine._core",
        sources=[
            "svcj_engine/_core.pyx", 
            "svcj_engine/svcjmath.c"
        ],
        # CRITICAL FIX: Explicitly add both NumPy and Local paths here
        include_dirs=[numpy.get_include(), source_dir],
        language="c"
    )
]

# 3. Setup with cythonize
setup(
    name="svcj_engine",
    version="1.0.0",
    packages=["svcj_engine"],
    # Use cythonize to ensure .pyx is compiled to .c correctly
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
    zip_safe=False,
)