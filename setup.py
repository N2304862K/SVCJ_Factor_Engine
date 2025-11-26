# setup.py
from setuptools import setup, Extension, find_packages

# The C extension now lives inside the 'svcj_fast_factors' package
extensions = [
    Extension(
        # The full import path for the compiled module
        "svcj_fast_factors.wrapper", 
        sources=[
            "svcj_fast_factors/wrapper.pyx", 
            "svcj_fast_factors/src/svcjmath.c"
        ], 
        # Tell the compiler where to find the header file
        include_dirs=["svcj_fast_factors/src"],
        extra_compile_args=["-O3"]
    )
]

# Read the contents of the README file for a long description
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='svcj-fast-factors', 
    version='1.0.0',        
    author="N2304862K",
    description="A high-performance C/Cython SVCJ factor generation library.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/N2304862K/SVCJ_Factor_Engine",
    
    # This automatically finds the 'svcj_fast_factors' directory
    packages=find_packages(),
    
    # This tells the build system to compile the C/Cython code
    ext_modules=extensions,
    
    # This tells the build system to include non-Python files (specified in MANIFEST.in)
    include_package_data=True,
    
    # These are the packages a user needs to RUN the code
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
    zip_safe=False # Recommended for packages with C extensions
)
