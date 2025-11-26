import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# 1. Custom Builder to handle NumPy import safely
class BuildExt(build_ext):
    def run(self):
        import numpy
        # Add NumPy headers
        self.include_dirs.append(numpy.get_include())
        # Add the package directory itself so .h files are found
        self.include_dirs.append(os.path.join(os.path.dirname(__file__), "svcj_estimator"))
        super().run()

# 2. Define Extension (Note: No 'src' path, no '-O3' flag)
extensions = [
    Extension(
        name="svcj_estimator._core",
        sources=[
            "svcj_estimator/_core.pyx",
            "svcj_estimator/svcjmath.c"
        ],
        # Removing -O3 ensures Windows compatibility
        language="c"
    )
]

# 3. Setup
setup(
    name="svcj_estimator",
    version="0.1.0",
    packages=["svcj_estimator"],
    ext_modules=extensions,
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
)