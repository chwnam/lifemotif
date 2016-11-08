from datetime import date
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch

from .services import IndexService
from .models import MidIndex, Profile, TidIndex


class IndexServiceTest(TestCase):

    def setUp(self):

        # dummy user
        self.user = User.objects.create(
            is_superuser=False,
            username='test',
            email='test@gmail.com',
            is_staff=False,
            is_active=True
        )

        # dummy user's profile
        self.profile = Profile.objects.create(
            label_id='Label_1',
            user=self.user
        )

        # patch for gmail_api
        gmail_api_patcher_config = {
            'messages_list.return_value': {
                'messages': [
                    {'id': '500', 'threadId': '500', },
                    {'id': '410', 'threadId': '400', },
                    {'id': '400', 'threadId': '400', },
                    {'id': '310', 'threadId': '300', },
                    {'id': '300', 'threadId': '300', },
                    {'id': '220', 'threadId': '200', },
                    {'id': '210', 'threadId': '200', },
                    {'id': '200', 'threadId': '200', },
                    {'id': '101', 'threadId': '100', },
                    {'id': '100', 'threadId': '100', },
                ],
                'nextPageToken': '',
                'resultSizeEstimate': 10
            },
            'messages_get.return_value': {
                'payload': {
                    'headers': [
                        {'name': 'Date', 'value': 'Mon, 7 Nov 2016 12:05:18 -0600 (CST)'},
                        {'name': 'To', 'value': 'test@gmail.com'}
                    ]
                }
            }
        }
        self.gmail_api_patcher = patch('emails.providers.gmail.api.GmailApi', **gmail_api_patcher_config)

        # gmail api is a kind of Mock class, not a real one.
        self.gmail_api = self.gmail_api_patcher.start()
        self.addCleanup(self.gmail_api_patcher.stop)

        # create IndexService instance
        self.index_service = IndexService(self.gmail_api, self.profile)

        # patch for self.index_service.get_latest_mid()
        self.get_latest_mid_patcher = patch.object(self.index_service, 'get_latest_mid', return_value=int('101', 16))
        self.get_latest_mid_patcher.start()
        self.addCleanup(self.get_latest_mid_patcher.stop)

    def test_fetch_messages_list(self):
        # IndexService.get_latest_mid
        # GmailApi.messages_list
        output = self.index_service.fetch_messages_list()

        # id 101, and 100 should be excluded.
        self.assertEqual(len(output), 8, 'Number of total output is incorrect.')

    def test_extract_diary_dates(self):
        # GmailApi.message_get function is called.
        output = self.index_service.extract_diary_dates([(101, 100), (100, 100)])

        self.assertEqual(len(output), 1, 'Only one element must be found in \'output\' dict object.')
        self.assertIn(100, output, 'mid \'100\' is an alarm mail index, so a date should be extracted.')
        self.assertIsInstance(output[100], date, 'date extraction in not correct.')

    def test_update_index(self):
        self.index_service.update_index()

        # threadId 500, 400, 300, and 200 will be created.
        self.assertEqual(TidIndex.objects.filter(profile=self.profile).count(), 4, 'TidIndex count mismatch.')

        # mid 410, 310, 220, and 210 will be created.
        self.assertEqual(MidIndex.objects.filter(
            tid_index__profile=self.profile).count(), 4, 'MidIndex count mismatch.')

        # date is thought not to be important after it is successfully parsed, so its test is skipped.

    def test_reset_index(self):

        t_test = TidIndex.objects.create(tid=1000, diary_date=date.today(), profile=self.profile)
        MidIndex.objects.create(mid=1001, tid_index=t_test)

        self.index_service.reset_index()

        self.assertEqual(
            TidIndex.objects.filter(profile=self.profile).count(), 0, 'TidIndex reset is incomplete.')

        self.assertEqual(
            MidIndex.objects.filter(tid_index__profile=self.profile).count(), 0, 'MidIndex reset is incomplete.')
