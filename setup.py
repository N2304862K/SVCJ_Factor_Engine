# File: setup.py (Corrected)

from setuptools import setup, Extension
# DO NOT import cythonize here. Let setuptools handle it.
import numpy

# Define the C extension module. Setuptools will see the ".pyx" extension
# and know to use Cython to build it.
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
    version='1.0.1', # Bump version for new release
    author='N2304862K',
    description='A high-speed engine for generating SVCJ risk factors from financial time series data.',
    packages=['svcj_engine'],
    # Simply pass the list of extensions. setuptools handles the rest.
    ext_modules=extensions,
    install_requires=[
        'numpy>=1.20.0',
        'pandas>=1.3.0',
    ],
    # This keyword is a fallback for older versions of pip/setuptools
    # to ensure they install Cython before trying to build.
    setup_requires=['cython', 'numpy'],
    zip_safe=False,
)