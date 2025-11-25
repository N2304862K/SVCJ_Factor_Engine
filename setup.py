# svcj_fast_factors/setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension(
        "svcj_wrapper",                      
        sources=["svcj_wrapper.pyx", "src/svcjmath.c"], 
        include_dirs=[numpy.get_include(), "src"], 
        extra_compile_args=["-O3"]
    )
]

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='svcj_fast_factors',
    version='0.1.1', 
    author="N2304862K", 
    description="A high-performance C/Cython SVCJ factor generation library.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/N2304862K/SVCJ_Factor_Engine",
    
    ext_modules=cythonize(extensions),
    install_requires=[
        "numpy>=1.20",
        "pandas>=1.3",
        "yfinance>=0.1.70",
        "Cython>=0.29"
    ],
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry"
    ],
    python_requires='>=3.8',
)
