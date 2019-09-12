import os
import sys
import unittest
from unittest.mock import MagicMock

sys.path += os.pardir
from nespy import NesPy


class TestStringMethods(unittest.TestCase):

    def test_if_parser_gets_filename(self):
        nespy = NesPy()
        parser = nespy.parse_arguments(['--file', 'filename.bin'])
        self.assertEqual(parser.file, 'filename.bin')

    # def test_if_loader_is_called(self):
    #     memory_mapper = MagicMock()
    #     nespy = NesPy(memory_mapper)
    #     nespy.parse_arguments(['--file', 'filename.bin'])
    #
    #     memory_mapper.__init__.assert_called_with()


if __name__ == '__main__':
    unittest.main()
