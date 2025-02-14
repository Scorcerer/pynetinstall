import os
import sys
import logging
import argparse
import logging.config

from pynetinstall.flash import FlashInterface, FatalError, AbortFlashing

parser = argparse.ArgumentParser(__package__)
parser.add_argument("-c", "--config", default="/etc/pynetinstall.ini", help="set location of configuration file")
parser.add_argument("-i", "--interface", default="eth0", help="ethernet interface to listen on")
parser.add_argument("-l", "--logging", default=None, help="python logging configuration")
parser.add_argument("-v", "--verbose", action="count", default=0, help="enable verbose output")
parser.add_argument("-1", "--oneshot", action="store_true", help="exit after flashing once")
args = parser.parse_args()

# default to ERROR+WARNING, each -v increases the verbosity (INFO, DEBUG). must not set to NOTSET (0), or logger gets disabled.
levels = sorted([e for e in logging._levelToName.keys() if e > 0], reverse=True)
verbosity = levels[min(len(levels)-1, levels.index(logging.WARNING) + args.verbose)]
if not args.logging:
    args.logging = os.path.join(os.path.dirname(__file__), "logging.ini")
logging.config.fileConfig(args.logging)

try:
    fl_dev = FlashInterface(args.interface, args.config, log_level=verbosity)

    if args.oneshot:
        fl_dev.flash_once()
    else:
        fl_dev.flash_until_stopped()
except FatalError as e:
    parser.error(e)
except AbortFlashing as e:
    sys.exit(1)
except KeyboardInterrupt as e:
    sys.exit(130)
