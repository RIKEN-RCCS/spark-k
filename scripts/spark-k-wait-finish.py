#!/usr/bin/env python

"""
Command to wait until all applications finish.  It returns 0, or 1 on
error.  It checks responses from http UI.
"""

import sys
import urllib2
import json
import time
import argparse
import logging
import itertools

FORMAT = '%(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
LOG = logging.getLogger(__name__)


class WaitCommand():
    """ Command to wait until no pending jobs exist. """

    __parser = argparse.ArgumentParser()
    __parser.add_argument('--debug',
                          action='store_true',
                          help=argparse.SUPPRESS)
    __parser.add_argument('--host', type=str, default='localhost')
    __parser.add_argument('--port', type=int, default=8080)
    __parser.add_argument('--interval', type=int, default=3)
    __parser.add_argument('--retrys', type=int, default=0)

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
    def run(cls):
        """ Waits until no workers are available. """

        args = cls.__parse_args()

        if args.debug:
            LOG.setLevel(logging.DEBUG)

        url = 'http://{}:{}/api/v1/applications/'.format(args.host, args.port)
        req = urllib2.Request(url)

        if args.retrys == 0:
            repeater = itertools.repeat(True)
        else:
            repeater = itertools.repeat(True, args.retrys)

        LOG.debug('Wait for applications finish.')
        for _ in repeater:
            try:
                response = urllib2.urlopen(req)
            except URLError, e:
                LOG.error('Bad url "{}".'.format(url))
                return 1
            except urllib2.HTTPError as e:
                LOG.error('Bad connection: {}.'.format(str(e)))
                return 1
            LOG.debug('Master response: code={}.'.format(response.getcode()))
            body = response.read()
            try:
                applications = json.loads(body)
            except ValueError, e:
                LOG.error('Bad response from url "{}".'.format(url))
                LOG.exception(e)
                return 1
            if applications is None:
                LOG.error('No applications information.')
                return 1

            LOG.debug('Master response: {}.'.format(applications))
            n = ([any(attempt.get('completed', False)
                      for attempt in app['attempts'])
                  for app in applications]).count(False)
            if n == 0:
                LOG.debug('All applications completed.')
                return 0
            LOG.debug('Not completed applications: {}.'.format(n))
            time.sleep(args.interval)
        LOG.error('Retry limit reached.')
        return 1


if __name__ == '__main__':
    v = WaitCommand.run()
    sys.exit(v)
