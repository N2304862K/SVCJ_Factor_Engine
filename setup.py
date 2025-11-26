# File: setup.py (Corrected)

from setuptools import setup, Extension
import numpy

# Define the C extension module. setuptools automatically detects the .pyx
# file and uses the Cython from pyproject.toml to build it.
extensions = [
    Extension(
        "svcj_engine.svcj_wrapper", 
        sources=[
            "svcj_engine/svcj_wrapper.pyx", 
            "svcj_engine/svcjmath.c"
        ], 
        include_dirs=[numpy.get_include()],
        extra_compile_args=["-O3"]
    )
]

setup(
    name='svcj_factor_engine',
    version='1.0.2', # Bump version for the fix
    author='N2304862K',
    description='A high-speed engine for generating SVCJ risk factors from financial time series data.',
    packages=['svcj_engine'],
    # Simply list the extensions. Do NOT use setup_requires.
    ext_modules=extensions,
    install_requires=[
        'numpy>=1.20.0',
        'pandas>=1.3.0',
    ],
    zip_safe=False,
)