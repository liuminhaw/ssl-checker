# -*- encoding: utf-8 -*-


import sys, os
import datetime, json
import requests
import argparse

from checker_pkg import checker_conf
from checker_pkg import ssl_check
from checker_pkg import mailer_sendgrid
from module_pkg import logging_class as logcl


VERSION = 'v0.1.1'
LOG_DIR = os.path.join(os.getcwd(), 'logs')

logger = logcl.PersonalLog('checker', LOG_DIR, frequency='day')

# matched_sites structure
# {
#     'recipient1': {
#         'x-days': ['site-url1', 'site-url2', ...], 
#         'y-days': ['site-url1', 'site-url2', ...],
#         ...
#     },
#     'recipient2': {
#         'x-days': ['site-url1', 'site-url2', ...],
#         ...
#     },
#     ...
# }
matched_sites = {}

def check_matching(recipient, days_left, site_data):
    """
    Params:
        recipient - mail receiver
        days_left - number of days left before expiration
        site_data - single site object json from sites.json 
    """
    # print(site_data)
    config_days = site_data['alert-days']
    url = site_data['site-url']

    for days in config_days:
        if days_left == int(days):
            if recipient not in matched_sites:
                matched_sites[recipient] = {}
            if days not in matched_sites[recipient]:
                matched_sites[recipient][days] = []
            matched_sites[recipient][days].append(url)


if __name__ == '__main__':
    CONFIG = 'conf.json'
    SITES_CONFIG = 'sites.json'

    # arguments definition
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-V', '--version', action='version', version='%(prog)s {}'.format(VERSION))
    args = arg_parser.parse_args()

    # Check for config file existence
    if not os.path.isfile(CONFIG):
        print('[INFO] {} file not exist.'.format(CONFIG))
        sys.exit(1)
    if not os.path.isfile(SITES_CONFIG):
        print('[INFO] {} file not exists.'.format(SITES_CONFIG))
        sys.exit(1)

    # Test global config - conf.json
    try:
        mail_info = checker_conf.Config(CONFIG)
    except checker_conf.configError as err:
        logger.warning(err)
        sys.exit(11)

    # Test config - sites.json
    sites_info = checker_conf.SitesConfig(SITES_CONFIG)
    try:
        sites_info.validation()
    except checker_conf.configError as err:
        logger.warning(err)
        sys.exit(11)

    # Start checker information
    logger.info('\n============ SSL Check ============\n')

    # with open(FILENAME) as json_file:
        # sites_data = json.load(json_file)
    for site_name in sites_info.configs:

        # Test https
        url = sites_info.configs[site_name]['site-url']
        try:
            requests.get('https://{}'.format(url), verify=True)
        except requests.exceptions.SSLError:
            logger.info('Site {} no https support'.format(url))
            print('')
            continue

        # Check ssl certificate expiration date
        host_info = ssl_check.check_it_out(url, 443)
        recent_time = datetime.datetime.now()
        delta_time = host_info.cert.not_valid_after - recent_time
        info_str = '\nSite URL: {}\n'.format(url)
        info_str += 'Alt name: {}\n'.format(ssl_check.get_alt_names(host_info.cert))
        info_str += 'Issuer: {}\n'.format(ssl_check.get_issuer(host_info.cert))
        info_str += '{} day(s) left\n'.format(delta_time.days)
        logger.info(info_str)

        # Check custom recipient
        try:
            recipient = sites_info.configs[site_name]['recipient']
        except KeyError:
            recipient = mail_info.recipient

        # Check alert days matching
        check_matching(recipient, delta_time.days, sites_info.configs[site_name])

    # Sending mail
    if bool(matched_sites):
        for address, matches in matched_sites.items():
            new_mail = mailer_sendgrid.Sender(
                mail_info.api_key, 
                mail_info.sender, 
                address, 
                mail_info.subject)

            new_mail.construct_content(matches)
            try:
                new_mail.send_mail()
                logger.info('Send mail to {} succeeded'.format(address))
            except mailer_sendgrid.mailError as err:
                logger.warning('Failed to send mail: {}'.format(err))




