from django.db import models
from django.contrib.auth.models import User


class TidIndex(models.Model):
    """
    Alarm mail is generally discarded, but it has an important property, diary date.
    Because diary date comes from MIME header, all alarm mails should be fetched, and parsed first.
    """
    tid = models.IntegerField(
        primary_key=True,
        verbose_name='thread ID',
        help_text='Thread ID in Gmail. If a groups of mails have an identical number, then they are threaded.'
    )

    diary_date = models.DateField(
        db_index=True
    )

    profile = models.ForeignKey('Profile', related_name='gmail_tids')

    def __str__(self):
        return '0x{0:x}, {1}'.format(self.tid, self.diary_date)


class MidIndex(models.Model):
    """
    Model for reply mails. An alarm mail, whose mid is equals to tid, will not be stored here.
    """
    mid = models.IntegerField(
        primary_key=True,
        verbose_name='message ID',
        help_text='Message ID in Gmail. This is a unique 64 bit integer for one account.'
    )

    tid_index = models.ForeignKey('TidIndex', related_name='gmail_mids')


class Profile(models.Model):
    """
    Gmail specific user profile
    """
    label_id = models.CharField(
        max_length=32,
        help_text='A unique string to identify an label. e.g. Label_40. Up to 32 characters.'
    )

    user = models.ForeignKey(User, related_name='gmail_profiles')
