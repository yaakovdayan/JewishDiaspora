from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from authtools.models import AbstractEmailUser
from django.utils.translation import ugettext as _


class IntendType(object):
    NA = 1
    BORROW = 2
    DONATE = 3

    choices = (
        (NA, _('Not specified')),
        (BORROW, _('Borrow')),
        (DONATE, _('Donate')),
    )


class User(AbstractEmailUser):
    full_name = models.CharField(_('Full name'), max_length=255, blank=True)
    phone = models.CharField(_('Phone'), max_length=255, blank=True)

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def send_registration_email(self, password):
        return send_mail(
            _('New account at Jewish Diaspora'),
            '{}\n{}: {}\n{}: {}'.format(_('Hi, a new account was created for you, login info'), _('Email'), self.email,
                                        _('Password'), password),
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )


class ArtifactContact(models.Model):
    submitted_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(_('Name'), max_length=250)
    email = models.EmailField(_('Email'), max_length=250)
    phone = models.CharField(_('Phone'), max_length=250)
    artifact_info = models.TextField(_('Artifact info'), blank=True, null=True)
    intend_type = models.PositiveSmallIntegerField(_(''), choices=IntendType.choices, default=IntendType.NA)

    def __str__(self):
        return u'{}: {}'.format(self.submitted_at, self.name)
