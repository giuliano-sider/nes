from ppu import Ppu
from memory_mapper import MemoryMapper
import os
import numpy as np

DEFAULT_iNES_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_utils', 'acopalices.bin')

# Acopalices game related constants.

BIG_ROACH_TOP_LEFT_PATTERN = np.array([
    [0, 0, 0, 0, 2, 3, 3, 3],
    [0, 0, 0, 0, 1, 2, 2, 2],
    [3, 0, 0, 0, 1, 2, 2, 2],
    [0, 3, 0, 0, 1, 1, 2, 2],
    [3, 0, 3, 0, 0, 1, 2, 2],
    [0, 3, 0, 3, 0, 1, 1, 2],
    [0, 0, 3, 0, 3, 0, 1, 1],
    [0, 3, 0, 3, 0, 3, 0, 1]
])
BIG_ROACH_TOP_LEFT_PATTERN_TILE_INDEX = 0

def CreateTestPpu(iNES_file=DEFAULT_iNES_FILE):
    """Return a valid ppu for testing purposes. Any valid iNES file name or valid sequence of bytes read from such a file will work."""
    return Ppu(MemoryMapper(iNES_file))