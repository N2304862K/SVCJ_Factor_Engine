# File: setup.py (Definitive Fix)

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# --- Lazy Cythonization ---
# This wrapper function ensures that cythonize is only called when
# the extension is actually being built, not at import time.
def lazy_cythonize(extensions):
    def _cythonize(dist, attr, value):
        from Cython.Build import cythonize
        dist.ext_modules = cythonize(extensions, force=True)
    return _cythonize

# A custom build_ext class to handle lazy NumPy inclusion
class CustomBuildExt(build_ext):
    def finalize_options(self):
        build_ext.finalize_options(self)
        # Prevent `numpy` from being imported before it's installed.
        # This is a critical step for modern packaging.
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
        # Note: include_dirs is now handled by CustomBuildExt
        extra_compile_args=["-O3"]
    )
]

setup(
    name='svcj_factor_engine',
    version='1.0.3', # Bump version for the definitive fix
    author='N2304862K',
    description='A high-speed engine for generating SVCJ risk factors from financial time series data.',
    packages=['svcj_engine'],
    # ext_modules is now set lazily via the setup attribute
    install_requires=[
        'numpy>=1.20.0',
        'pandas>=1.3.0',
    ],
    # The key change: use setup attributes to control the build process
    setup_requires=['cython', 'numpy'],
    cmdclass={'build_ext': CustomBuildExt},
    attrs={'ext_modules': lazy_cythonize(extensions)},
    zip_safe=False,
)