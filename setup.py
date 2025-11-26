# File: setup.py (The Definitive Solution)

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext

# --- The "Numpy-Aware" Build Extension ---
# This class ensures that numpy is imported only when it's absolutely needed.
# It's the canonical way to solve the "numpy.get_include()" problem during
# a pip install of a Cython package.
class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from being imported before it's installed.
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())

# Define the C extension module
extensions = [
    Extension(
        "svcj_engine.svcj_wrapper", 
        sources=[
            "svcj_engine/svcj_wrapper.pyx", 
            "svcj_engine/svcjmath.c"
        ], 
        # The include_dirs will be populated by the class above at build time
        extra_compile_args=["-O3"]
    )
]

# Read the contents of the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='svcj_factor_engine',
    version='1.2.0', # Bump version for the critical build fix
    author='N2304862K',
    description='A high-speed engine for generating SVCJ risk factors from financial time series data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/N2304862K/SVCJ_Factor_Engine",
    packages=['svcj_engine'],
    # Tell setuptools to use our custom build_ext class
    cmdclass={'build_ext': build_ext},
    ext_modules=extensions,
    install_requires=[
        'numpy>=1.20.0',
        'pandas>=1.3.0',
    ],
    # setup_requires is still a good fallback for some environments
    setup_requires=['numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    zip_safe=False,
)