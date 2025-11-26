# File: setup.py
# This script defines the package and its compiled extensions.
# It is designed to be "NumPy-aware" by deferring the import of numpy.

from setuptools import setup, Extension

# A small trick to defer the numpy import until after it has been
# installed by the build backend (pip).
class get_numpy_include:
    def __str__(self):
        import numpy
        return numpy.get_include()

# Define the C extension module
extensions = [
    Extension(
        "svcj_engine.svcj_wrapper", 
        sources=[
            "svcj_engine/svcj_wrapper.pyx", 
            "svcj_engine/svcjmath.c"
        ], 
        include_dirs=[get_numpy_include()],
        extra_compile_args=["-O3"]
    )
]

# Read the contents of the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='svcj_factor_engine',
    version='1.1.0', # It's good practice to bump the version
    author='N2304862K',
    description='A high-speed engine for generating SVCJ risk factors from financial time series data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/N2304862K/SVCJ_Factor_Engine",
    packages=['svcj_engine'],
    ext_modules=extensions,
    install_requires=[
        'numpy>=1.20.0',
        'pandas>=1.3.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    zip_safe=False,
)