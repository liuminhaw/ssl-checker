# -*- coding:UTF-8 -*-

# Exit status:
#   _VALUE_ - _EXPLANATION_

# Standard library imports
import os

# Third party library imports
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Local application imports
# import self defined applications here

class Sender:
    def __init__(self, key, sender, recipient, subject):
        self.api_key = key
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.content = ''

    def construct_content(self, alerts_data):
        """
        Params:
            alert_data - dict of VALUE sites that will expire in KEY days
            # {'days': ['site_url1', 'site_url2'], ...}
        """
        self.content = '<p>SSL certificates expiration alert</p>'

        for days, sites_list in alerts_data.items():
            self.content += '<h4>Expire in {} day(s)</h4><ul>'.format(days)
            for site in sites_list:
                self.content += '<li>{}</li>'.format(site)
            self.content += '</ul>'

    def send_mail(self):
        message = Mail(
            from_email=self.sender,
            to_emails=self.recipient,
            subject=self.subject,
            html_content=self.content)

        try:
            sg = SendGridAPIClient(self.api_key)
            sg.send(message)
            #response = sg.send(message)
            #print(response.status_code)
            #print(response.body)
            #print(response.headers)
        except Exception as e:
            raise mailError(e)


# Exceptions
class mailError(Exception):
    """
    Mailing exception
    """
    pass