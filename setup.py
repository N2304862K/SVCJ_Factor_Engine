# File: setup.py

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext

# This class ensures numpy is available when the extension is being built,
# solving the classic "numpy.get_include()" problem during installation.
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
        # The include_dirs will be populated by the class above at build time.
        extra_compile_args=["-O3"]
    )
]

# Read the README for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='svcj_factor_engine',
    version='1.2.1', # It's good practice to bump the version for each release
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
    # This is a fallback for older build environments
    setup_requires=['numpy'],
    python_requires='>=3.8',
    zip_safe=False,
)