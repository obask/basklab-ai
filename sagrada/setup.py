from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("board.pyx", annotate=True, language_level=3), requires=['Cython']
)
