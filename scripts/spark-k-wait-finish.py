#!/usr/bin/env python

"""
Command to wait until all applications finish.  It returns 0, or 1 on
error.  It wait indefinitely by default.  It checks all entries to
become "completed: true" in responses from HTTP UI
(http://master:8080/api/v1/applications/).  Normally, it immediately
returns, because spark-submit waits for itself.
"""

import sys
import urllib2
import json
import time
import argparse
import logging
import itertools


FORMAT = '%(filename)s-%(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)


class WaitCommand():
    """Command to wait until no pending applications exist."""

    __parser = argparse.ArgumentParser()
    __parser.add_argument('--terse', action='store_true',
                          help=argparse.SUPPRESS)
    __parser.add_argument('--host', type=str, default='localhost')
    __parser.add_argument('--port', type=int, default=8080)
    __parser.add_argument('--interval', type=int, default=10)
    __parser.add_argument('--retrys', type=int, default=0)

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
    def run(cls):
        """Waits until all executors finish."""

        args = cls.__parse_args()

        if args.terse:
            logger.setLevel(logging.WARNING)
        else:
            logger.setLevel(logging.INFO)

        url = 'http://{}:{}/api/v1/applications/'.format(args.host, args.port)
        req = urllib2.Request(url)

        logger.info('Wait for applications finish.')
        if args.retrys == 0:
            repeater = itertools.repeat(True)
        else:
            repeater = itertools.repeat(True, args.retrys)
        for _ in repeater:
            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError as e:
                logger.error('Bad connection: {}.'.format(str(e)))
                return 1
            except urllib2.HTTPError as e:
                logger.error('Bad response: {}.'.format(str(e)))
                return 1
            logger.info('Master response: code={}.'.format(response.getcode()))
            body = response.read()
            try:
                applications = json.loads(body)
            except ValueError as e:
                logger.error('Bad response: {}.'.format(str(e)))
                logger.exception(e)
                return 1
            if applications is None:
                logger.error('No applications information.')
                return 1

            ##logger.debug('Master response: {}.'.format(applications))
            # (sum flattens list of lists).
            completeds = sum([[attempt.get('completed', False)
                                  for attempt in app['attempts']]
                                 for app in applications], [])
            n = completeds.count(False)
            logger.info('Completed applications: {}.'.format(completeds))
            if n == 0:
                logger.info('All applications completed.')
                return 0
            time.sleep(args.interval)
        logger.error('Retry limit reached.')
        return 1


if __name__ == '__main__':
    v = WaitCommand.run()
    sys.exit(v)
