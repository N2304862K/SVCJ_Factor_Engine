# File: setup.py

from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

# Define the C extension module that needs to be compiled
extensions = [
    Extension(
        # The name of the resulting module that will be imported in Python
        "svcj_engine.svcj_wrapper", 
        # List of all source files required for compilation
        sources=[
            "svcj_engine/svcj_wrapper.pyx", 
            "svcj_engine/svcjmath.c"
        ], 
        # Include directory for NumPy headers, necessary for Cython
        include_dirs=[numpy.get_include()],
        # Compiler flags for maximum optimization
        extra_compile_args=["-O3"]
    )
]

setup(
    name='svcj_factor_engine',
    version='1.0.0',
    author='N2304862K',
    description='A high-speed engine for generating SVCJ risk factors from financial time series data.',
    # Specify the packages to be included in the distribution
    packages=['svcj_engine'],
    # Tell setuptools to use Cython to build the extensions
    ext_modules=cythonize(extensions),
    # Define dependencies required for the package to run
    install_requires=[
        'numpy>=1.20.0',
        'pandas>=1.3.0',
    ],
    zip_safe=False,
)