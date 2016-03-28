#!/usr/bin/env python

"""
Wait until Spark workers connect to Spark master
"""

import sys
import urllib2
import time
import argparse
import logging
from itertools import repeat
from xml.etree.ElementTree import fromstring

FORMAT = '%(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
LOG = logging.getLogger(__name__)

PORT_MAX = 65535

class WaitCommand():
    """ wait command """

    __parser = argparse.ArgumentParser()

    __parser.add_argument('-d', '--debug',
                            action='store_true',
                            help=argparse.SUPPRESS)

    __parser.add_argument('--host', type=str, default='localhost')

    __parser.add_argument('--port', type=int, default=8080)

    __parser.add_argument('--interval', type=int, default=3)

    __parser.add_argument('--retry-max-initial', type=int, default=3)

    __parser.add_argument('--retry-max', type=int, default=0)

    __parser.add_argument('--node-num', type=int, default=0)


    @classmethod
    def __parse_args(cls):
        """ Parse argument and check their values """

        args = cls.__parser.parse_args(sys.argv[1:])

        if args.port < 0:
            cls.__parser.error('port is too small')

        if args.port > PORT_MAX:
            cls.__parser.error('port is too large')

        if args.retry_max < 0:
            cls.__parser.error('retry_max should be positive')

        return args


    @classmethod
    def get_worker_number(cls, html):
        """
        Get a number of alive workers from a html string

        Expects '<li><strong>Alive Workers:</strong> 1</li>'

        """
        elem = fromstring(html).findall('.//li')
        lst = filter(lambda x: len(x) > 0 and x[0].text == 'Alive Workers:',
                     elem)
        if len(lst) == 0:
            raise ValueError('Unexpected HTML')
        elif len(lst[0]) == 0:
            raise ValueError('Unexpected HTML')
        elif not lst[0][0].tail.strip().isdigit():
            raise ValueError('Unexpected Value')
        else:
            return int(lst[0][0].tail)


    @classmethod
    def run(cls):
        """ Run the wait command """

        args = cls.__parse_args()

        if args.debug:
            LOG.setLevel(logging.DEBUG)

        url = 'http://{}:{}/'.format(
            args.host, args.port)
        req = urllib2.Request(url)

        if args.retry_max_initial:
            repeater = repeat(True, args.retry_max_initial)
        else:
            repeater = repeat(True)

        response = None
        for _ in repeater:
            time.sleep(args.interval)
            try:
                response = urllib2.urlopen(req)
            except urllib2.HTTPError as e:
                LOG.warn('url "{}" is not available'.format(url))
                continue
            except urllib2.URLError, e:
                LOG.warn('failed to open {}'.format(url))
                continue
            break
        
        if response is None:
            LOG.error('failed to connect to the Master UI')
            return 1

        if args.retry_max:
            repeater = repeat(True, args.retry_max)
        else:
            repeater = repeat(True)

        for _ in repeater:
            try:
                response = urllib2.urlopen(req)
            except urllib2.HTTPError as e:
                LOG.error('url "{}" is not available'.format(url))
                return 1
            except urllib2.URLError, e:
                LOG.error('failed to open {}'.format(url))
                return 1
            LOG.debug('status code is {}'.format(response.getcode()))

            body = response.read()
            LOG.debug('Server responce is {}'.format(body))

            try:
                workers_number = cls.get_worker_number(body)
            except ValueError, e:
                LOG.error('invalid data {}'.format(url))
                if args.debug:
                    LOG.exception(e)
                return 1

            LOG.debug('#worker is "{}"'.format(workers_number))
            if workers_number >= args.node_num:
                LOG.debug('All expected workers are connected to master')
                return 0
            time.sleep(args.interval)


if __name__ == '__main__':
    sys.exit(WaitCommand.run())

