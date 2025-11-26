import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# --- 1. The Lazy NumPy Fix ---
class BuildExt(build_ext):
    def run(self):
        # Only import numpy here, inside the build process
        import numpy
        
        # Add NumPy headers to include_dirs
        self.include_dirs.append(numpy.get_include())
        
        # Add the package directory to include_dirs so svcjmath.h is found
        # We use abspath to ensure it works regardless of where pip runs from
        package_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "svcj_engine")
        self.include_dirs.append(package_dir)
        
        super().run()

# --- 2. Define the Extension ---
extensions = [
    Extension(
        name="svcj_engine._core",
        sources=[
            "svcj_engine/_core.pyx",
            "svcj_engine/svcjmath.c"
        ],
        # Do not put include_dirs here; BuildExt handles it
        # No extra compile args (safe for all platforms)
        language="c"
    )
]

# --- 3. Setup ---
setup(
    name="svcj_engine",
    version="1.0.0",
    packages=["svcj_engine"],
    ext_modules=extensions,
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
)