import argparse
import sys


class NesPy:

    def parse_arguments(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('--file', '-f', help='path for nes bin file')
        answer = parser.parse_args(args)
        return answer


if __name__ == '__main__':
    nesPy = NesPy()
    parser = nesPy.parse_arguments(sys.argv[1:])
