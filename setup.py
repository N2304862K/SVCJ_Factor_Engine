# setup.py
from setuptools import setup, Extension
import numpy

# Define the C extension module
extensions = [
    Extension(
        "svcj_wrapper",                      
        sources=["svcj_wrapper.pyx", "src/svcjmath.c"], 
        include_dirs=[numpy.get_include(), "src"], 
        extra_compile_args=["-O3"]
    )
]

# Read the contents of your README file for the package description
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='svcj_engine',
    version='0.2.0', # Incremented version
    author="N2304862K", # Your GitHub username
    description="A high-performance C/Cython SVCJ factor generation library.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/N2304862K/SVCJ_Factor_Engine",
    
    ext_modules=extensions,
    
    install_requires=[
        "numpy>=1.20",
        "pandas>=1.3",
        "yfinance>=0.1.70"
    ],
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
