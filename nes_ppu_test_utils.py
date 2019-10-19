from ppu import Ppu
from memory_mapper import MemoryMapper
from log import FAKE_LOGGER
from instructions import instructions
import os

DEFAULT_iNES_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_utils', 'brk')


def CreateTestPpu(iNES_file=DEFAULT_iNES_FILE):
    """Return a valid ppu for testing purposes. Any valid iNES file name or valid sequence of bytes read from such a file will work."""
    return Ppu(MemoryMapper(iNES_file))