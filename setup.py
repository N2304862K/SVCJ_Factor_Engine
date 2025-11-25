from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

extensions = [Extension("svcj_wrapper", sources=["svcj_wrapper.pyx", "svcjmath.c"], include_dirs=[numpy.get_include()], extra_compile_args=["-O3"])]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='svcj-factor-engine',
    version='1.0.0',
    author='JTPC',
    author_email='tpcheung@gmail.com',
    description='A high-performance engine for generating SVCJ factors.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/N2304862K/SVCJ_Factor_Engine.git',
    packages=find_packages(),
    ext_modules=cythonize(extensions),
    install_requires=[
        'numpy',
        'pandas'
    ],
    
    setup_requires=[
        'setuptools>=18.0',
        'cython>=0.29',
        'numpy'
    ],
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    
    python_requires='>=3.8',
)
