# svcj_fast_factors/setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

# Define the C extension module
extensions = [
    Extension(
        "svcj_wrapper",                      # The name of the Python module
        sources=["svcj_wrapper.pyx", "src/svcjmath.c"], # Source files
        include_dirs=[numpy.get_include(), "src"], # Include paths for .h and .c
        extra_compile_args=["-O3"]           # Optimization flag for speed
    )
]

setup(
    name='svcj_fast_factors',
    version='0.1.0',
    packages=['svcj_fast_factors'], # This allows it to be installed as a package
    ext_modules=cythonize(extensions),
    install_requires=[
        "numpy>=1.20",
        "pandas>=1.3",
        "yfinance>=0.1.70",
        "Cython>=0.29"
    ],
    author="JTPC",
    description="A high-performance C/Cython SVCJ factor generation library.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/N2304862K/SVCJ_Factor_Engine", # Replace with your repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=3.8',
)
