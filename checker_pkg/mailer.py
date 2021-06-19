# -*- coding:UTF-8 -*-

# Exit status:
#   _VALUE_ - _EXPLANATION_

# Standard library imports
import os

# Third party library imports
import boto3
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Local application imports
# import self defined applications here

class Sender():
    def __init__(self, sender, recipient, subject):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject

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


class SendgridSender(Sender):
    def __init__(self, key, sender, recipient, subject):
        Sender.__init__(self, sender, recipient, subject)
        self.api_key = key
        self.content = ''

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


class SesSender(Sender):
    def __init__(self, key_id, secret_key, region, sender, recipient, subject):
        Sender.__init__(self, sender, recipient, subject)
        self.key_id = key_id
        self.secret_key = secret_key
        self.region = region

    def send_mail(self):
        session = boto3.session.Session(
            aws_access_key_id=self.key_id, 
            aws_secret_access_key=self.secret_key,
            region_name=self.region)
        ses_client = session.client('ses')

        try:
            response = ses_client.send_email(
                Source=self.sender,``
                Destination={
                    'ToAddresses': [
                        self.recipient
                    ],
                },
                Message={
                    'Subject': {
                        'Data': self.subject,
                        'Charset': 'UTF-8'
                    },
                    'Body': {
                        'Html': {
                            'Data': self.content,
                            'Charset': 'UTF-8'
                        }
                    }
                }
            )
        except Exception as e:
                raise mailError(e)


# Exceptions
class mailError(Exception):
    """
    Mailing exception
    """
    pass