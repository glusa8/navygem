from navygem.settings import GOOGLE_RECAPTCHA_SECRET_KEY
from navygem.settings import GOOGLE_RECAPTCHA_VERIFICATION_URL
from navygem.settings import MAILGUN_EMAIL_VALIDATION_URL
from navygem.settings import MAILGUN_PUBLIC_API_KEY
import re
import requests
from utils.email_domain_blacklist import BLACKLISTED_EMAIL_DOMAINS

def verify_recaptcha(g_recaptcha_response):
    r = requests.post(
        GOOGLE_RECAPTCHA_VERIFICATION_URL,
        data={
            'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': g_recaptcha_response
        }
    )

    response = r.json()
    return response['success']


def validate_email(email):
    r = requests.get(
        MAILGUN_EMAIL_VALIDATION_URL,
        params={
            'api_key': MAILGUN_PUBLIC_API_KEY,
            'address': email
        }
    )
    response = r.json()
    return response['is_valid']

def validate_email_form(email):
    return re.match('^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$', email)

def is_blacklisted_email(email):
    return email.split('@')[1] in BLACKLISTED_EMAIL_DOMAINS
