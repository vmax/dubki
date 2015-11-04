#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    A module providing functionality for logging
"""

from datetime import datetime
import os


def log(filename, message):
    """
        Writes log messages to files

        Args:
            filename(str): log file name
            message(str): message to write
    """
    path = os.path.join(os.getcwd(), 'logs/')
    path = os.path.join(path, filename)
    with open(path, 'a') as logfile:
        logfile.write('[{date}]: {msg}\n'.format(
            date=datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
            msg=message))


def make_logger(filename):
    """
        Returns a logger for certain filename

        Args:
            filename(str): log file name

        Returns:
            function that writes its argument to specified file
    """
    return lambda message: log(filename, message)
