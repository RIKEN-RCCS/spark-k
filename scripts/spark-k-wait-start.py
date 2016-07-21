#!/usr/bin/env python

"""
Command to wait until all workers join to a master.  It returns 0, or
1 on error.  It checks responses from http UI.  It retries for 120
seconds by default.
"""

import sys
import urllib2
import time
import argparse
import logging
import itertools
import xml.etree.ElementTree as ET

FORMAT = '%(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
LOG = logging.getLogger(__name__)


class WaitCommand():
    """ Command to wait until all workers connect to a master. """

    __parser = argparse.ArgumentParser()
    __parser.add_argument('workers', type=int,
                          help='number of workers to wait')
    __parser.add_argument('--debug',
                          action='store_true',
                          help=argparse.SUPPRESS)
    __parser.add_argument('--host', type=str, default='localhost')
    __parser.add_argument('--port', type=int, default=8080)
    __parser.add_argument('--interval', type=int, default=3)
    __parser.add_argument('--retrys', type=int, default=40)

    @classmethod
    def __parse_args(cls):
        """ Parses arguments. """

        PORT_MAX = 65535
        args = cls.__parser.parse_args(sys.argv[1:])
        if args.port < 0:
            cls.__parser.error('port is too small')
        if args.port > PORT_MAX:
            cls.__parser.error('port is too large')
        if args.retrys < 0:
            cls.__parser.error('retrys should be positive')
	args.debug = True
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
            LOG.warn('No Alive Workers field.')
            return 0
        elif len(elems[0]) == 0:
            raise Error('(never)')
        elif not elems[0][0].tail.strip().isdigit():
            LOG.error('Bad Alive Workers field: {}.'.format(elems[0][0].text))
            raise ValueError('Bad Alive Workers field.')
        else:
            return int(elems[0][0].tail)

    @classmethod
    def run(cls):
        """ Waits until all workers become available. """

        args = cls.__parse_args()

        if args.debug:
            LOG.setLevel(logging.DEBUG)

        url = 'http://{}:{}/'.format(args.host, args.port)
        req = urllib2.Request(url)

        LOG.debug('Wait for workers to join: workers={}.'.format(args.workers))
        if args.retrys == 0:
            repeater = itertools.repeat(True)
        else:
            repeater = itertools.repeat(True, args.retrys)
        for _ in repeater:
            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
                LOG.error('Bad url "{}".'.format(url))
                return 1
            except urllib2.HTTPError as e:
                LOG.warn('Bad connection: {}.'.format(str(e)))
                time.sleep(args.interval)
                continue
            LOG.debug('Master response: code={}.'.format(response.getcode()))
            body = response.read()
            ##LOG.debug('Master response: {}.'.format(body))
            try:
                nworkers = cls.get_alive_workers_field_from_response(body)
            except ValueError, e:
                LOG.error('Bad response from url "{}".'.format(url))
                LOG.exception(e)
                return 1

            LOG.debug('Current workers: workers={}.'.format(nworkers))
            if nworkers >= args.workers:
                LOG.debug('All expected workers joined to master.')
                return 0
            time.sleep(args.interval)
        LOG.error('Retry limit reached.')
	return 1


if __name__ == '__main__':
    v = WaitCommand.run()
    sys.exit(v)
