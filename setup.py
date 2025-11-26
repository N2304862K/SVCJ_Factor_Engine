import numpy
from setuptools import setup, Extension
from Cython.Build import cythonize

# Define the C Extension
extensions = [
    Extension(
        name="svcj_estimator._core",  # Compiles to svcj_estimator._core
        sources=[
            "src/svcj_estimator/_core.pyx", 
            "src/svcj_estimator/svcjmath.c"
        ],
        include_dirs=[numpy.get_include()],  # Solves 'numpy/arrayobject.h' error
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
        extra_compile_args=["-O3"], # Optimization flags
        language="c"
    )
]

setup(
    name="svcj_estimator",
    packages=["svcj_estimator"],
    package_dir={"": "src"},
    ext_modules=cythonize(
        extensions, 
        compiler_directives={'language_level': "3"} # Force Python 3
    ),
)