#!/usr/bin/env python

"""
Wait command for all workers join to a master.  It returns 0, or 1 on
error.  It checks responses from HTTP UI (http://master:8080/).  It
retries in 600 seconds by default.
"""

import sys
import urllib2
import time
import argparse
import logging
import itertools
import xml.etree.ElementTree as ET


FORMAT = '%(filename)s-%(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)


class WaitStart():
    """Wait command until all workers connect to a master."""

    __parser = argparse.ArgumentParser()
    __parser.add_argument('workers', type=int,
                          help='number of workers to wait')
    __parser.add_argument('--terse', action='store_true',
                          help=argparse.SUPPRESS)
    __parser.add_argument('--host', type=str, default='localhost')
    __parser.add_argument('--port', type=int, default=8080)
    __parser.add_argument('--interval', type=int, default=10)
    __parser.add_argument('--retrys', type=int, default=60)

    @classmethod
    def __parse_args(cls):
        """Parses arguments."""

        args = cls.__parser.parse_args(sys.argv[1:])
        if args.port < 0:
            cls.__parser.error('port is too small')
        if args.port > 65535:
            cls.__parser.error('port is too large')
        if args.retrys < 0:
            cls.__parser.error('retrys should be positive')
        args.terse = False
        return args

    @classmethod
    def get_alive_workers_field_from_response(cls, html):
        """
        Gets the alive workers field from a string HTML.  It expects
        '<li><strong>Alive Workers:</strong> 1</li>'.  It returns 0
        when no fields exist.
        """
        elems0 = ET.fromstring(html).findall('.//li')
        elems = filter(lambda x: len(x) > 0 and x[0].text == 'Alive Workers:',
                       elems0)
        if len(elems) == 0:
            logger.warning('No Alive Workers field.')
            return 0
        elif len(elems[0]) == 0:
            raise Error('(never)')
        elif not elems[0][0].tail.strip().isdigit():
            logger.error('Bad Alive Workers field: {}.'
                         .format(elems[0][0].text))
            raise ValueError('Bad Alive Workers field.')
        else:
            return int(elems[0][0].tail)

    @classmethod
    def run(cls):
        """Waits until all workers become available."""

        args = cls.__parse_args()

        if args.terse:
            logger.setLevel(logging.WARNING)
        else:
            logger.setLevel(logging.INFO)

        url = 'http://{}:{}/'.format(args.host, args.port)
        req = urllib2.Request(url)

        logger.info('Wait for workers to join: workers={}.'
                    .format(args.workers))
        if args.retrys == 0:
            repeater = itertools.repeat(True)
        else:
            repeater = itertools.repeat(True, args.retrys)
        for _ in repeater:
            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError as e:
                logger.warning('Bad connection: {}.'.format(str(e)))
                time.sleep(args.interval)
                continue
            except urllib2.HTTPError as e:
                logger.warning('Bad response: {}.'.format(str(e)))
                time.sleep(args.interval)
                continue
            logger.info('Master response: code={}.'.format(response.getcode()))
            body = response.read()
            ##logger.debug('Master response: {}.'.format(body))
            try:
                nworkers = cls.get_alive_workers_field_from_response(body)
            except ValueError as e:
                logger.error('Bad response: {}.'.format(str(e)))
                logger.exception(e)
                return 1

            logger.info('Current workers: workers={}.'.format(nworkers))
            if nworkers >= args.workers:
                logger.info('All expected workers joined to master.')
                return 0
            time.sleep(args.interval)
        logger.error('Retry limit reached.')
        return 1


if __name__ == '__main__':
    v = WaitStart.run()
    sys.exit(v)
