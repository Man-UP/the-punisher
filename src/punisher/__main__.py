from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

from punisher.gui import mainloop

def main(argv=None):
    if argv is None:
        argv = sys.argv
    mainloop()
    return 0

if __name__ == '__main__':
    exit(main())

