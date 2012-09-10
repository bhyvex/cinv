#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 2012 Nico Schottelius (nico-sexy at schottelius.org)
#
# This file is part of sexy.
#
# sexy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sexy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sexy. If not, see <http://www.gnu.org/licenses/>.
#
#

VERSION="2.0"

import subprocess

class Error(Exception):
    """Base class for fallback of all exceptions"""
    pass

def commandline():
    """Parse command line"""
    import argparse

    # Construct parser others can reuse
    parser = {}
    # Options _all_ parsers have in common
    parser['loglevel'] = argparse.ArgumentParser(add_help=False)
    parser['loglevel'].add_argument('-d', '--debug',
        help='Set log level to debug', action='store_true',
        default=False)
    parser['loglevel'].add_argument('-v', '--verbose',
        help='Set log level to info, be more verbose',
        action='store_true', default=False)

    # Main subcommand parser
    parser['main'] = argparse.ArgumentParser(description='sexy ' + VERSION,
        parents=[parser['loglevel']])
    parser['main'].add_argument('-V', '--version',
        help='Show version', action='version',
        version='%(prog)s ' + VERSION)
    parser['main'].epilog = "Get sexy at http://www.nico.schottelius.org/software/sexy/"
    parser['mainsub'] = parser['main'].add_subparsers(title="Commands")

    # net-ipv4
    parser['net-ipv4'] = {}
    parser['net-ipv4']['main'] = parser['mainsub'].add_parser('net-ipv4', 
        parents=[parser['loglevel']])
    parser['net-ipv4']['sub'] = parser['net-ipv4']['main'].add_subparsers(title="net-ipv4 commands")

    parser['net-ipv4']['add'] = parser['net-ipv4']['sub'].add_parser('add', 
        parents=[parser['loglevel']])
    parser['net-ipv4']['add'].add_argument('subnet', help='Subnet to delete')

    parser['net-ipv4']['del'] = parser['net-ipv4']['sub'].add_parser('del', 
        parents=[parser['loglevel']])

    parser['net-ipv4']['del'].add_argument('subnet', help='Subnet to delete')

    args = parser['main'].parse_args(sys.argv[1:])

    # Loglevels are handled globally in here and debug wins over verbose
    if args.verbose:
        logging.root.setLevel(logging.INFO)
    if args.debug:
        logging.root.setLevel(logging.DEBUG)

    log.debug(args)
    args.func(args)

if __name__ == "__main__":
    # Sys is needed for sys.exit()
    import sys

    sexypythonversion = '3.2'
    if sys.version < sexypythonversion:
        print('Sexy requires Python >= ' + sexypythonversion +
            ' on the source host.', file=sys.stderr)
        sys.exit(1)


    exit_code = 0

    try:
        import logging
        import os
        import re

        # Ensure our /lib/ is included into PYTHON_PATH
        sys.path.insert(0, os.path.abspath(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), '../lib')))

        # And now import our stuff
        #import sexy

        log = logging.getLogger("sexy")

        logging.basicConfig(format='%(levelname)s: %(message)s')

        commandline()

    except KeyboardInterrupt:
        pass

    #except sexy.Error as e:
    #    log.error(e)
    #    exit_code = 1

    # Determine exit code by return value of function
    #sys.exit(exit_code)