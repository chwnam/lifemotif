from os.path import join as path_join
from gzip import open as gzip_open


def save_message(mid, message, store_path):
    """
    :type  mid:        int   message id
    :type  message:    str   raw MIME message
    :param store_path: str   path to store
    :return:
    """
    path = path_join(store_path, '%x.gz' % mid)
    with gzip_open(path, 'wb') as f:
        f.write(message)


def load_message(mid, store_path):
    """
    :type mid:         int    message id
    :type store_path:  str    path to load
    :return:
    """
    path = path_join(store_path, '%x.gz' % mid)
    with gzip_open(path, 'rb') as f:
        message = f.read()
    return message
