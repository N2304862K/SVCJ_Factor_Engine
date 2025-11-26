from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

# Define the C extension module that will be compiled
extensions = [
    Extension(
        # The name must match the .pyx file and the package structure
        "svcj_engine._svcj_wrapper", 
        sources=[
            "src/svcj_engine/_svcj_wrapper.pyx", 
            "src/svcj_engine/svc_jcore.c"
        ],
        include_dirs=[numpy.get_include()],
        extra_compile_args=["-O3"] # Maximum optimization for speed
    )
]

# The setup call
setup(
    ext_modules=cythonize(extensions),
    # Most metadata is now in pyproject.toml
)```

#### 5. `src/svcj_engine/__init__.py`
This file makes the `svcj_engine` directory a Python package and provides the clean, high-level `generate_factors` function to the user.

```python
# src/svcj_engine/__init__.py

# Import the core function from the compiled Cython module
# and expose it at the top level of the package.
from ._svcj_wrapper import generate_svcj_factor_matrix as generate_factors

# This allows the user to simply write:
# from svcj_engine import generate_factors