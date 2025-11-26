import os
import numpy
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# Custom builder to handle numpy headers safely
class BuildExt(build_ext):
    def run(self):
        self.include_dirs.append(numpy.get_include())
        # FIX: Add the local source directory so compiler finds svcjmath.h
        self.include_dirs.append(os.path.join(os.path.dirname(__file__), "src", "svcj_estimator"))
        super().run()

extensions = [
    Extension(
        name="svcj_estimator._core", 
        sources=[
            "src/svcj_estimator/_core.pyx",
            "src/svcj_estimator/svcjmath.c"
        ],
        # Do not define include_dirs here, the BuildExt handles it
        extra_compile_args=["-O3"],
        language="c"
    )
]

setup(
    name="svcj_estimator",
    version="0.1.0",
    description="High-performance SVCJ factor engine",
    packages=["svcj_estimator"],
    package_dir={"": "src"},
    ext_modules=extensions,
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
)