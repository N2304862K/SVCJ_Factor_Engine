import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# The "Deferred Import" Pattern
class BuildExt(build_ext):
    def run(self):
        import numpy
        # Add NumPy headers to the include path dynamically
        self.include_dirs.append(numpy.get_include())
        # Add the local source directory so svcjmath.h is found
        self.include_dirs.append(os.path.join(os.path.dirname(__file__), "svcj_engine"))
        super().run()

# Define Extension WITHOUT include_dirs (BuildExt handles it)
extensions = [
    Extension(
        name="svcj_engine._core",
        sources=[
            "svcj_engine/_core.pyx",
            "svcj_engine/svcjmath.c"
        ],
        # Safe compile args for Linux/Mac/Windows
        extra_compile_args=[], 
        language="c"
    )
]

setup(
    name="svcj_engine",
    version="1.0.0",
    packages=["svcj_engine"],
    ext_modules=extensions, # Pass the extension objects
    cmdclass={'build_ext': BuildExt}, # Use our custom builder
    zip_safe=False,
)