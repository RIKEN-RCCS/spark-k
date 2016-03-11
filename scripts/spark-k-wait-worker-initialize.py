#!/usr/bin/env python

import os
import sys
import time
import argparse
import logging
import time
from subprocess import Popen, PIPE

from itertools import repeat

FORMAT = '%(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
LOG = logging.getLogger(__name__)


def tailf(target, interval):
    """ read line from the file like tail -f """
    with open(target, 'r') as file:
        while True:
            where = file.tell()
            line = file.readline()
            if not line:
                time.sleep(interval)
                file.seek(where)
            else:
                yield line


class Timer():
    def __init__(self, after=1000):
        self.base_time = time.time()
        self.after = after

        self.upper_limit = self.base_time + self.after


    def reach_timeout():
        return time.time() > self.upper_limit



class Command():
    """ wait command """

    __parser = argparse.ArgumentParser()

    __parser.add_argument('-d', '--debug',
                            action='store_true',
                            help=argparse.SUPPRESS)

    __parser.add_argument('--interval', type=int, default=3)

    __parser.add_argument('--timeout', type=int, default=300)

    __parser.add_argument('spark_master_log', action='store', type=str)


    @classmethod
    def __parse_args(cls):
        """ Parse argument and check their values """

        args = cls.__parser.parse_args(sys.argv[1:])

        if args.interval < 0:
            cls.__parser.error('interval should be positive')

        return args


    @classmethod
    def get_K_nodes(cls):
        """ get K nodes """
        p = Popen('mpiexec /work/system/bin/msh hostname',
                  stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        return out.split()


    @classmethod
    def run(cls):
        """ Run the this command """

        args = cls.__parse_args()

        if args.debug:
            LOG.setLevel(logging.DEBUG)

        nodes = cls.get_K_nodes()

        count = 0

        timer = Timer(after=args.timeout)
        for line in tailf(args.spark_master_log, args.interval):
            if 'Registering worker' in line:
                count = count + 1
                if len(nodes) == counts:
                    break
            elif 'Removing worker' in line:
                count = count - 1
            if timer.reach_timeout():
                LOG.warn('Reached timeout!')
                break

        return 0


if __name__ == '__main__':
    sys.exit(Command.run())



