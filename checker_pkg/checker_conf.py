# -*- coding:UTF-8 -*-

# Exit status:
#   _VALUE_ - _EXPLANATION_

# Standard library imports
# import standard libraries here
import json

# Third party library imports
# import third party libraries here

# Local application imports
# import self defined applications here



class Config:
    def __init__(self, config_file):
        """
        Params:
            config_file - json configuration file for ssl_checker
        Errors:
            configError - confiugration error
        """
        self.config_file = config_file
        with open(self.config_file) as json_file:
            configs = json.load(json_file)
            try:
                self.method = configs['method']
            except KeyError:
                raise configError('method not set in config file')

        if self.method.lower() == 'sendgrid':
            try:
                self._sendgrid(configs['sendgrid'])
            except KeyError:
                raise configError('sendgrid block not set in config file')
        else:
            raise configError('configError: [{}] block not set in config file'.format(self.method.lower()))

    def _sendgrid(self, configs):
        """
        Params: 
            configs - sendgrid data block parsed from config file
        """
        try:
            self.api_key = configs['key']
        except KeyError:
            raise configError('config key not set')
        try:
            self.sender = configs['sender']
        except KeyError:
            raise configError('config sender not set')
        try:
            self.recipient = configs['recipient']
        except KeyError:
            raise configError('config recipient not set')
        try:
            self.subject = configs['subject']
        except KeyError:
            raise configError('config subject not set')
        


# Exceptions
class configError(Exception):
    """
    Base class of config exception
    """
    pass