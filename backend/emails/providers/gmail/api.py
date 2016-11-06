from backend.auth_dishes import BaseAuthDish


class GmailApi(object):

    url_base = 'https://www.googleapis.com/gmail/v1/users'

    def __init__(self, auth_dish):
        """
        :type auth_dish: BaseAuthDish
        """
        self.auth_dish = auth_dish

    def _make_request(self, url, *args, **kwargs):
        """
         - method
         - params
         - json
        :param url:
        :param args:
        :param kwargs:
        :return:
        """
        request_func = self.auth_dish.get_request_func()

        return request_func(url,
                            headers=self.auth_dish.default_request_header,
                            *args, **kwargs)

    def get_labels(self):
        endpoint = '%s/%s/labels' % (self.url_base, self.auth_dish.user_email)
        return self._make_request(endpoint)

    def messages_list(self, *args, **kwargs):
        """
        reference: https://developers.google.com/gmail/api/v1/reference/users/messages/list
        usage example:
            api.message_list(
                params={
                    'labelIds': label_id,
                    'nextPageToken': next_page_token,
                }
            )

        :return:
        """
        endpoint = '%s/%s/messages' % (self.url_base, self.auth_dish.user_email)
        return self._make_request(endpoint, *args, **kwargs)

    def messages_get(self, mid, *args, **kwargs):
        """
        reference: https://developers.google.com/gmail/api/v1/reference/users/messages/get
        usage example:
            api.message_get(
                gmail_message_id,
                params={
                    'format': 'raw',
                },
            )

        :type mid: int
        :return:
        """
        endpoint = '%s/%s/messages/%x' % (self.url_base, self.auth_dish.user_email.uid, mid)
        return self._make_request(endpoint, *args, **kwargs)
