IncludeDirListODE = ["cpp_lib/ODE"]
IncludeDirListDAE = ["cpp_lib/DAE"]
IncludeDirListGillespie = ["cpp_lib/Gillespie"]
#numpy_include = ['/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/numpy/core/include/']

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


sourcefilesODE = ['ODESolver.pyx', 'cpp_lib/ODE/ODESolver.cpp']
sourcefilesDAE = ['DAESolver.pyx', 'cpp_lib/DAE/DAESolver.cpp']
sourcefilesGillespie = ['GillespieSolver.pyx', 'cpp_lib/Gillespie/Gillespie.cpp']

setup(
    cmdclass = dict(build_ext = build_ext),
    ext_modules = [
        Extension(
            'ODESolver',
            sourcefilesODE,
            language='c++',
            include_dirs = IncludeDirListODE + numpy_include,
            libraries = ['gsl', 'gslcblas'],
            library_dirs = ['/usr/lib']
            )
        ]
    )

setup(
    cmdclass = dict(build_ext = build_ext),
    ext_modules = [
        Extension(
            'DAESolver',
            sourcefilesDAE,
            language='c++',
            include_dirs = IncludeDirListDAE + numpy_include,
            libraries = ['gsl', 'gslcblas'],
            library_dirs = ['/usr/lib']
            )
        ]
    )


import numpy
setup(
    cmdclass = dict(build_ext = build_ext),
    ext_modules = [
        Extension(
            'GillespieSolver',
            sourcefilesGillespie,
            include_dirs = IncludeDirListGillespie + numpy_include,
            language='c++',
            libraries = ['gsl', 'gslcblas'],
            )
        ]
    )
