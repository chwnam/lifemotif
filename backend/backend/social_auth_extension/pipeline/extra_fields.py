from time import time


def set_updated_at(details, *args, **kwargs):
    """
    Pipeline function to add extra information about when the social auth profile has been updated.

    Args:
        details (dict): dictionary of information about the user

    Returns:
        dict: updated details dictionary
    """
    details['updated_at'] = int(time())

    return details
