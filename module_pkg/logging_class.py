"""
Program:
    Personal defined logging class
Author:
    haw
Version:
    1.2.0
"""

import sys, os, errno
import logging, datetime
from pathlib import Path

class PersonalLog():
    """
    Params:
        prog_name - name to show on log files
        directory - path to save log files (Home directory is set as default path)
        frequency - how frequent do the files rotate (month[default] or day)
    """

    def __init__(self, prog_name, directory='', frequency='month'):
        self.logger = logging.getLogger(prog_name)

        # Log file name
        if frequency.lower() == 'day':
            filename = '{}-{}.log'.format(datetime.date.today().strftime('%Y-%m-%d'), prog_name)
        else:
            filename = '{}-{}.log'.format(datetime.date.today().strftime('%Y-%m'), prog_name)

        # logging target directory
        if os.path.isdir(directory):
            self.log_dir = directory
        else:
            self.log_dir = os.path.join(str(Path.home()), 'python_log')

        # logging target file
        self.log_file = os.path.join(self.log_dir, filename)

        # Make python_log directory if not exist
        os.makedirs(self.log_dir, exist_ok=True)

        # Set logger
        self.logger.setLevel(logging.DEBUG)

        # Log handlers
        format = logging.Formatter('%(asctime)-12s %(levelname)-8s %(name)-10s  %(message)-12s')
        file_handle = logging.FileHandler(self.log_file)
        file_handle.setFormatter(format)
        file_handle.setLevel(logging.INFO)

        std_handle = logging.StreamHandler()
        std_handle.setFormatter(format)
        std_handle.setLevel(logging.DEBUG)

        self.logger.addHandler(file_handle)
        self.logger.addHandler(std_handle)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


if __name__ == "__main__":
    # Testing logging_class
    # logging.disable(logging.DEBUG)

    log_test = PersonalLog('logging_class', frequency='day')

    log_test.debug('Debug Test')
    log_test.info('Info Test')
    log_test.warning('Warning Test')
    log_test.error('Error Test')
    log_test.critical('Critical Test')