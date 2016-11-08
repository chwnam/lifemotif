from datetime import datetime
from django.db.models import Max
from django.utils.timezone import get_default_timezone
from email.utils import mktime_tz, parsedate_tz
from logging import getLogger

from .models import MidIndex, TidIndex


class IndexService(object):

    def __init__(self, gmail_api, profile):
        """
        :type gmail_api: emails.providers.gmail.api.GmailApi
        :type profile: emails.providers.gmail.models.Profile
        """
        self.gmail_api = gmail_api
        self.profile = profile
        self.logger = getLogger(__name__)

    def update_index(self):

        self.logger.info(
            'updating index for profile id \'{} ({})\' has started'.format(self.profile.id, self.profile.label_id)
        )

        # fetch messages until the mid
        messages_list = self.fetch_messages_list()

        # extract diary dates
        diary_dates = self.extract_diary_dates(messages_list)

        # update tid index
        tid_indices = {}
        for tid, date in diary_dates.items():
            obj, created = TidIndex.objects.get_or_create(
                tid=tid,
                defaults={'tid': tid, 'diary_date': date, 'profile': self.profile, }
            )
            tid_indices[tid] = obj

        # update mid index
        # get_or_create() might be much safer than bulk_create() because update_index() method
        #  can be invoked twice or more against existing message items.
        for mid, tid in messages_list:
            if mid != tid:
                MidIndex.objects.get_or_create(
                    mid=mid,
                    tid_index=tid_indices[tid],
                    defaults={'mid': mid, 'tid_index': tid_indices[tid]}
                )

        self.logger.info(
            'updating index for profile id \'{} ({})\' finished'.format(self.profile.id, self.profile.label_id)
        )

        return True

    def reset_index(self):
        TidIndex.objects.filter(profile=self.profile).delete()

    def get_latest_mid(self):
        latest_mid = MidIndex.objects \
            .select_related('tid_index') \
            .filter(tid_index__profile=self.profile) \
            .aggregate(Max('mid'))['mid__max']

        return latest_mid or 0

    def fetch_messages_list(self):

        next_page_token = True
        latest_mid = self.get_latest_mid()
        output = []

        self.logger.debug(
            'fetch_messages_list of profile id \'{0} ({1})\' - resuming from \'{2} (0x{2:x})\''.format(
                self.profile.id,
                self.profile.label_id,
                latest_mid
            )
        )

        while next_page_token:
            response = self.gmail_api.messages_list(
                params={
                    'labelIds': self.profile.label_id,
                    'pageToken': next_page_token if type(next_page_token) != bool else ''
                }
            )
            self.logger.debug('message list API from google, {} items found'.format(response['resultSizeEstimate']))

            messages = response.get('messages', [])
            next_page_token = response.get('nextPageToken', '')

            for message in messages:
                mid = int(message['id'], 16)
                tid = int(message['threadId'], 16)
                if mid <= latest_mid:
                    self.logger.debug(
                        'mid={} <= latest_mid={}, fetch process is done.'.format(mid, latest_mid)
                    )
                    next_page_token = ''
                    break
                output.append((mid, tid))

        self.logger.info(
            'successfully fetched {} item(s) for profile id \'{} ({})\''.format(
                len(output),
                self.profile.id,
                self.profile.label_id
            )
        )

        return output

    def extract_diary_dates(self, messages_list):
        """
        Please be patient!
        It can take minutes because every alarm mail in the structure is going to be fetched
         to extract its date field within.

        :param messages_list:
        :return:
        """
        output = {}

        for mid, tid in messages_list:
            if mid != tid:
                continue

            self.logger.debug(
                'Extracting diary date from mid, tid {0} (0x{0:x})'.format(mid)
            )

            # the response is very simple
            # e.g.
            # {
            #   "payload": {
            #     "headers": [
            #       {
            #         "name": "Date",
            #         "value": "Mon, 7 Nov 2016 12:05:18 -0600 (CST)"
            #       }
            #     ]
            #   }
            # }
            response = self.gmail_api.messages_get(
                mid,
                params={
                    'format': 'metadata',
                    'metadataHeaders': 'Date',
                    'fields': 'payload/headers'
                }
            )

            date_text = None
            for header in response['payload']['headers']:
                if header.get('name') == 'Date':
                    date_text = header.get('value')
                    self.logger.debug('\'Date\' header found: {}'.format(date_text))
                    break
            assert(date_text is not None)

            output[mid] = datetime.fromtimestamp(
                mktime_tz(parsedate_tz(date_text)), get_default_timezone()
            ).date()

        self.logger.info(
            'Date headers successfully extracted from {} alarm mails'.format(len(output))
        )

        return output
