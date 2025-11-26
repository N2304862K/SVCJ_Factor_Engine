# File: setup.py (Definitive Fix)

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# This custom build_ext class is the key to solving the build dependency issues.
# It ensures that Cython and NumPy are imported only when they are actually needed.
class CustomBuildExt(build_ext):
    def run(self):
        # Lazy import of Cython and run the cythonize command
        from Cython.Build import cythonize
        # This converts the .pyx file into a .c file
        self.extensions = cythonize(self.extensions, force=True, language_level=3)
        # Continue with the standard build process
        build_ext.run(self)
        
    def finalize_options(self):
        build_ext.finalize_options(self)
        # This is a standard hack to prevent NumPy from being imported before
        # it has been installed by the build process.
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        # Add the NumPy include directory to the compiler's search path
        self.include_dirs.append(numpy.get_include())

# Define the C extension module
extensions = [
    Extension(
        "svcj_engine.svcj_wrapper", 
        sources=[
            "svcj_engine/svcj_wrapper.pyx", 
            "svcj_engine/svcjmath.c"
        ], 
        # The include_dirs is now handled dynamically by CustomBuildExt
        extra_compile_args=["-O3"]
    )
]

setup(
    name='svcj_factor_engine',
    version='1.1.0', # Bump version for the definitive fix
    author='N2304862K',
    description='A high-speed engine for generating SVCJ risk factors from financial time series data.',
    packages=['svcj_engine'],
    # The custom build class is registered with setuptools here
    cmdclass={'build_ext': CustomBuildExt},
    # The extensions are passed directly to setuptools
    ext_modules=extensions,
    install_requires=[
        'numpy>=1.20.0',
        'pandas>=1.3.0',
    ],
    zip_safe=False,
)