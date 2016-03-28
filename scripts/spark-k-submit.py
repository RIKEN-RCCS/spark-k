#!/usr/bin/env python

"""
Wrapper script of spark-submit for the K environment
"""


import os
import sys
import json
import time
import logging
import subprocess

FORMAT = '%(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
LOG = logging.getLogger(__name__)

KEI_SPARK_INITIALIZE = "spark-k-initialize"

KEI_SPARK_FINALIZE = "spark-k-finalize"

SPARK_SUBMIT = "spark-submit"

class SubmitCommand():
    """ command """


    @classmethod
    def usage(cls):
        """ Print usage """
        command = os.path.basename(sys.argv[0])
        print >> sys.stderr, "Usage: {0} [-h|--help] spark_arguments ..." \
            .format(command)
        print >> sys.stderr, "	-h,--help		Show this help"


    @classmethod
    def modify_spark_arguments(cls, dummy_args):
        """ Replace spark option for K"""
        spark_args = [
            '--master', '${SPARK_MASTER}',
            ]

        for idx, arg in enumerate(dummy_args):
            if arg is None:
                continue
            elif arg in ('--master'):
                if idx + 1 < len(dummy_args) and dummy_args[idx + 1][0] != '-':
                    LOG.warn('remove "{0} {1}" from option'.format(
                        arg, dummy_args[idx + 1]))
                    dummy_args[idx + 1] = None
                else:
                    LOG.warn('remove "{0}" from option'.format(arg))
            elif arg.endswith('.jar') or arg.endswith('.py'):
                # Don't modify options after a jar file or a python file.
                # They are options for Spark Driver
                spark_args.extend(dummy_args[idx:])
                break
            else:
                spark_args.append(arg)
        return spark_args


    @classmethod
    def gen_spark_command(cls, argv):
        """ Generate spark command for K"""

        dirname = os.path.dirname(argv[0])

        initializer = os.path.join(dirname, KEI_SPARK_INITIALIZE)
        finalizer = os.path.join(dirname, KEI_SPARK_FINALIZE)

        dummy_args = argv[1:]
        if len(dummy_args) and (dummy_args[0] == "-h" or dummy_args[0] == "--help"):
            cls.usage()
            sys.exit(1)

        spark_args = cls.modify_spark_arguments(dummy_args)

        spark_command = """
        (
        . {0} ;
        ${{SPARK_HOME}}/bin/spark-submit {1};
        . {2} ;
        )
        """.format(
            initializer,
            ' '.join(spark_args),
            finalizer)

        return spark_command


    @classmethod
    def run(cls):
        spark_command = cls.gen_spark_command(sys.argv)
        return subprocess.Popen(spark_command, shell=True).wait()


if __name__ == '__main__':
    sys.exit(SubmitCommand.run())
