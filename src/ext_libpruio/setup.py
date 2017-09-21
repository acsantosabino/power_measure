from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

setup(
    ext_modules = cythonize([
    Extension("pruio", ["pruio.pyx"],
              libraries=["pruio"])
    ])
)

# run "sudo  python setup.py build_ext -i" to build pruio module
