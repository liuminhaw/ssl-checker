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


class Config():
    def __init__(self, config_file):
        """
        Params:
            config_file - json configuration file
        """
        self.config_file = config_file

    def _key_error(self, configs, key, msg):
        """
        Params:
            configs - json data block
            key - parsing key value
            msg - output message if KeyError raised
        Return:
            parsed data value
        """
        try:
            config_value = configs[key]
        except KeyError:
            raise configError(msg)
        else:
            return config_value


class SendingConfig(Config):
    def __init__(self, config_file):
        """
        Params:
            config_file - json configuration file (conf.json)
        Errors:
            configError - configuration error
        """
        Config.__init__(self, config_file)
        with open(self.config_file, 'r') as json_file:
            configs = json.load(json_file)
            err_msg = 'mail-method not set in config file'
            self.method = self._key_error(configs, 'mail-method', err_msg)

        if self.method.lower() == 'sendgrid':
            err_msg = 'sendgrid block not set in config file'
            self._key_error(configs, 'sendgrid', err_msg)
            self._sendgrid(configs['sendgrid'])
        elif self.method.lower() == 'ses':
            err_msg = 'ses block not set in config file'
            self._key_error(configs, 'ses', err_msg)
            self._ses(configs['ses'])
        else:
            raise configError('configError: [{}] block not set in config file'.format(self.method.lower()))

    def _sendgrid(self, configs):
        """
        Params: 
            configs - sendgrid data block parsed from config file
        Errors:
            configError - configuration error
        """
        err_msg = 'config key not set'
        self.api_key = self._key_error(configs, 'key', err_msg) 
        err_msg = 'config sender not set'
        self.sender = self._key_error(configs, 'sender', err_msg) 
        err_msg = 'config recipient not set'
        self.recipient = self._key_error(configs, 'recipient', err_msg) 
        err_msg = 'config subject not set'
        self.subject = self._key_error(configs, 'subject', err_msg) 

    def _ses(self, configs):
        """
        Params:
            configs - aws ses data block parsed from config file
        Errors:
            configError - configuration error
        """
        err_msg = 'config key not set'
        self.key_id = self._key_error(configs, 'key', err_msg)
        err_msg = 'config secret not set'
        self.secret_key = self._key_error(configs, 'secret', err_msg)
        err_msg = 'config region not set'
        self.region = self._key_error(configs, 'region', err_msg)
        err_msg = 'config sender not set'
        self.sender = self._key_error(configs, 'sender', err_msg) 
        err_msg = 'config recipient not set'
        self.recipient = self._key_error(configs, 'recipient', err_msg) 
        err_msg = 'config subject not set'
        self.subject = self._key_error(configs, 'subject', err_msg) 


class SitesConfig(Config):
    def __init__(self, config_file):
        """
        Params:
            config_file - json configuration file (sites.json)
        Errors:
            configError - configuration error
        """
        Config.__init__(self, config_file)
        self.matched_sites = {}
        with open(self.config_file, 'r') as json_file:
            self.configs = json.load(json_file)

    def validation(self):
        """
        sites.conf configuration validation
        Errors:
            configError - configuration error
        """
        for site in self.configs:
            # Check key: site-domain
            err_msg = 'key [site-domain] not set for {}'.format(site)
            self._key_error(self.configs[site], 'site-domain', err_msg)
            # Check key: alert-days
            err_msg = 'key [alert-days] not set for {}'.format(site)
            self._key_error(self.configs[site], 'alert-days', err_msg)



# Exceptions
class configError(Exception):
    """
    Base class of config exception
    """
    pass