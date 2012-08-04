from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourceforGillespieSolver = ['./GillespieSolver.pyx', './Gillespie.cpp']

setup(
        cmdclass = dict(build_ext = build_ext),
        ext_modules = [
            Extension(
                'GillespieSolver',
                sourceforGillespieSolver,
                language='c++',
                libraries = ['libgsl.dylib'],

            )
        ]
    )
