from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy
import os

# Robustly find the README file
def get_long_description():
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    return "A high-performance C/Cython SVCJ factor generation library."

# Define the C extension module
extensions = [
    Extension(
        "svcj_wrapper",
        sources=["svcj_wrapper.pyx", "src/svcjmath.c"],
        include_dirs=[numpy.get_include(), "src"],
        extra_compile_args=["-O3"]
    )
]

setup(
    name='svcj_fast_factors',
    version='0.1.0', 
    ext_modules=cythonize(extensions),
    install_requires=[
        "numpy>=1.20",
        "pandas>=1.3",
        "yfinance>=0.1.70",
        "Cython>=0.29"
    ],
    author="N2304862K", 
    description="A high-performance C/Cython SVCJ factor generation library.",
    long_description=get_long_description(), # Use the safe function
    long_description_content_type='text/markdown',
    url="https://github.com/N2304862K/SVCJ_Factor_Engine", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires='>=3.8',
)
