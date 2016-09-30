from navygem.settings import DEFAULT_FROM_ADDRESS
from navygem.settings import MAILGUN_API_KEY
from navygem.settings import MAILGUN_SEND_EMAIL_URL
import requests
from requests.auth import HTTPBasicAuth

def send_email(to, subject, html):
    r = requests.post(
        MAILGUN_SEND_EMAIL_URL,
        data={
            'from': DEFAULT_FROM_ADDRESS,
            'to': to,
            'subject': subject,
            'html': html
        },
        auth=HTTPBasicAuth('api', MAILGUN_API_KEY)
    )
