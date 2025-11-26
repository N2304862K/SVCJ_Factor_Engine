import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# --- Custom Build Step to Handle NumPy Include Path ---
class BuildExt(build_ext):
    def run(self):
        import numpy
        self.include_dirs.append(numpy.get_include())
        super().run()

# --- Define Extension ---
# Note: We use relative paths assuming the 'src' layout
extensions = [
    Extension(
        name="svcj_estimator._core",
        sources=[
            "src/svcj_estimator/_core.pyx",
            "src/svcj_estimator/svcjmath.c"
        ],
        # We do NOT put include_dirs here; we handle it in BuildExt
        extra_compile_args=["-O3"], 
        language="c"
    )
]

# --- Main Setup ---
setup(
    name="svcj_estimator",
    packages=["svcj_estimator"],
    package_dir={"": "src"},
    ext_modules=extensions,
    cmdclass={'build_ext': BuildExt}, # Use our custom builder
    zip_safe=False,
)