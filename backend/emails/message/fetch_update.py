from base64 import urlsafe_b64decode
from datetime import datetime
from email.utils import mktime_tz, parsedate_tz

from . import archive
from emails.providers.gmail.models import TidIndex as GmailTidIndex
from emails.providers.gmail.models import MidIndex as GmailMidIndex
from emails.providers.gmail.api import GmailApi


class GmailFetchUpdate(object):

    def __init__(self, gmail_api, label_id):
        """
        :type gmail_api: GmailApi
        :type label_id: str
        """
        self.api = gmail_api
        self.label_id = label_id

    @staticmethod
    def _is_alarm_mail(mid, tid):
        return mid == tid

    @staticmethod
    def _is_reply_mail(mid, tid):
        return mid != tid

    def _scan_list_once(self, next_page_token=None):
        return self.api.messages_list(
            params={
                'labelIds': self.label_id,
                'nextPageToken': next_page_token,
            }
        )

    def _scan_list(self, latest_mid):
        output = []
        # type: bool | str
        next_page_token = True

        while next_page_token:
            # type: dict
            r = self._scan_list_once()
            # type: list
            messages = r['messages'] if 'messages' in r else []
            # type: str
            next_page_token = r['nextPageToken'] if 'nextPageToken' in r else ''

            for message in messages:  # type:dict
                mid = int(message['id'], 16)
                tid = int(message['threadId'], 16)

                if mid <= latest_mid:
                    next_page_token = False
                    break
                else:
                    output.append((mid, tid))

        return output

    def extract_date(self, mid):
        r = self.api.messages_get(
            mid,
            {
                'format': 'metadata',
                'metadataHeaders': 'Date',
                'fields': 'payload/headers'
            }
        )
        date_value = r['payload']['headers'][0]['value']
        timestamp = mktime_tz(parsedate_tz(date_value))
        return datetime.utcfromtimestamp(timestamp).date()

    def fetch_message(self, mid):
        r = self.api.messages_get(
            mid,
            {
                'format': 'raw',
                'fields': 'raw',
            }
        )
        return urlsafe_b64decode(r['raw']).decode('ascii')

    def update_index(self, latest_mid, store_path):

        structure = self._scan_list(latest_mid)

        # structure loop #1:
        #   update tid index using structure
        #   extract diary date from alarm mails
        GmailTidIndex.objects.bulk_create(
            [
                GmailTidIndex(tid=tid, diary_date=self.extract_date(mid))
                for mid, tid in structure
                if self._is_alarm_mail(mid, tid)
            ]
        )

        # structure loop #2:
        #   fetch raw mime message using mid
        #   update mid index
        GmailMidIndex.objects.bulk_create(
            [
                GmailMidIndex(mid=mid, tid__index_id=tid)
                for mid, tid in structure
                if self._is_reply_mail(mid, tid)
            ]
        )

        # structure loop #3:
        # archive reply mails
        for mid, tid in structure:
            if self._is_reply_mail(mid, tid):
                message = self.fetch_message(mid)
                archive.save_message(mid, message, store_path)
