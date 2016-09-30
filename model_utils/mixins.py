from __future__ import unicode_literals

from django.db import models
from random import SystemRandom
import string

class TimestampsMixin(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    time_edited = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True

class DeletionMixin(models.Model):
    is_deleted = models.BooleanField(default=False)
    time_deleted = models.DateTimeField(null=True)

    class Meta(object):
        abstract = True

class DeactivationMixin(models.Model):
    is_deactivated = models.BooleanField(default=False)
    time_deactivated = models.DateTimeField(null=True)

    class Meta(object):
        abstract = True

class CodeBase(models.Model):
    CODE_LENGTH = 256

    code = models.CharField(max_length=CODE_LENGTH)

    class Meta(object):
        abstract = True

    @classmethod
    def generate_code(cls, digits_only=False):
        choices = string.digits if digits_only else '{}{}{}'.format(
            string.ascii_lowercase,
            string.ascii_uppercase,
            string.digits
        )

        return ''.join(
            SystemRandom().choice(choices)
            for _
            in range(cls.CODE_LENGTH)
        )
