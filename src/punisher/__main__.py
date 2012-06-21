from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from argparse import ArgumentParser
import sys

from punisher.gui import mainloop

def build_argument_parser():
    argument_parser = ArgumentParser()
    add = argument_parser.add_argument

    add('-t', '--judgment-time',
        help='Judgment time in HH:MM (24-hour) format.')

    return argument_parser

def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = build_argument_parser().parse_args(args=argv[1:])

    if args.judgment_time:
        mainloop(time=args.judgment_time)
    else:
        mainloop()

    return 0

if __name__ == '__main__':
    exit(main())

