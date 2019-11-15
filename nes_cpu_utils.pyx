
import os

from cpu cimport Cpu
from log cimport CpuLogger

MOD_ABSOLUTE = 0x10000
MOD_ZERO_PAGE = 0x100

class CpuHalt(Exception):
    pass

 



