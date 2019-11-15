# OFF distutils: define_macros=CYTHON_TRACE_NOGIL=1

from distutils.core import setup
from Cython.Build import cythonize
import os

# Used for line tracing...
# from Cython.Compiler.Options import get_directive_defaults
# directive_defaults = get_directive_defaults()
# directive_defaults['linetrace'] = True
# directive_defaults['binding'] = True

# Run with: python3 setup.py build_ext --inplace
# See python setup.py build_ext --help 
# for more help

setup(
    ext_modules = cythonize(module_list = [
        "nes.pyx",
        "instructions.pyx", "Instructions/*.pyx",
        "cpu.pyx", "nes_cpu_utils.pyx",
        "ppu.pyx", "nes_ppu_utils.pyx",
        "memory_mapper.pyx",
        "log.pyx",
        # Tests:
        "nes_cpu_test_utils.pyx", "nes_ppu_test_utils.pyx",
        "ScreenPygame.pyx",
        "emulator_timing_measurements.pyx",
        "tst/*.pyx"],
        include_path = [os.path.abspath(os.path.dirname(__file__))],
        annotate=True,
        compiler_directives={
            'language_level' : "3",
            # 'linetrace' : True
        })
    )