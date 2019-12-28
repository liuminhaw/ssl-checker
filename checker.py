# -*- encoding: utf-8 -*-


import sys
import datetime, json
import requests

from checker_pkg import checker_conf
from checker_pkg import ssl_check
from checker_pkg import mailer_sendgrid

# matched_sites structure
# {'days': ['site-url1', 'site-url2'], ...}
matched_sites = {}


def check_matching(days_left, site_data):
    """
    Params:
        days_left - number of days left before expiration
        site_data - single site object json from sites.json 
    """
    print(site_data)
    config_days = site_data['alert-days']
    url = site_data['site-url']

    for days in config_days:
        if days_left == int(days):
            if days not in matched_sites:
                matched_sites[days] = []
            matched_sites[days].append(url)


if __name__ == '__main__':
    CONFIG = 'conf.json'
    FILENAME = 'sites.json'

    # TODO: Test global config (config.json)
    try:
        mail_info = checker_conf.Config(CONFIG)
    except checker_conf.configError as err:
        print(err)
        sys.exit(1)

    with open(FILENAME) as json_file:
        sites_data = json.load(json_file)
        for site_name in sites_data:
            # TODO: Test site config

            # Test https
            url = sites_data[site_name]['site-url']
            try:
                requests.get('https://{}'.format(url), verify=True)
            except requests.exceptions.SSLError:
                print('Site {} no https support'.format(url))
                print('')
                continue

            # Check ssl certificate expiration date
            host_info = ssl_check.check_it_out(url, 443)
            recent_time = datetime.datetime.now()
            delta_time = host_info.cert.not_valid_after - recent_time
            print('Site URL: {}'.format(url))
            print('Alt name: {}'.format(ssl_check.get_alt_names(host_info.cert)))
            print('Issuer: {}'.format(ssl_check.get_issuer(host_info.cert)))
            print('{} day(s) left'.format(delta_time.days))
            print('')

            # Check alert days matching
            check_matching(delta_time.days, sites_data[site_name])

    # Sending mail
    if bool(matched_sites):
        new_mail = mailer_sendgrid.Sender(
            mail_info.api_key, 
            mail_info.sender, 
            mail_info.recipient, 
            mail_info.subject)

        new_mail.construct_content(matched_sites)
        new_mail.send_mail()

            # Just for debugging
            # print(matched_sites)

