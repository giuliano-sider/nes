import os

from nes import Nes

DEFAULT_iNES_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_utils', 'acopalices.bin')

def CreateTestNes(iNES_file=DEFAULT_iNES_FILE):
    """Return a valid Nes instance for testing purposes. Any valid iNES file name or valid sequences of bytes read from such a file will work."""
    return Nes(iNES_file)