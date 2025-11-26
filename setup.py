import os
import numpy
from setuptools import setup, Extension
from Cython.Build import cythonize

# Absolute path to the local source directory
current_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.join(current_dir, "svcj_engine")

print(f"DEBUG: Building with include_dirs: {numpy.get_include()} and {source_dir}")

extensions = [
    Extension(
        name="svcj_engine._core",
        sources=[
            "svcj_engine/_core.pyx",
            "svcj_engine/svcjmath.c"
        ],
        include_dirs=[numpy.get_include(), source_dir],
        # These macros help avoid some numpy version conflicts
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
        language="c"
    )
]

setup(
    name="svcj_engine",
    version="1.0.0",
    packages=["svcj_engine"],
    ext_modules=cythonize(
        extensions, 
        compiler_directives={'language_level': "3"}
    ),
    zip_safe=False,
)