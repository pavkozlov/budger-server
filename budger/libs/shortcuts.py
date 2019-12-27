import re


def get_object_or_none(model, *args, **kwargs):
    """ Load object and return it or return None if there is no such object. """
    try:
        obj = model.objects.get(*args, **kwargs)
        return obj
    except model.DoesNotExist:
        return None


def can_be_int(s):
    if s is None:
        return False

    try:
        int(s)
        return True
    except ValueError:
        return False


def normalize_search_str(s):
    """
    Нормализация строки, применяемой в поисках.
    """
    if s is not None:
        norm = re.sub(r'[^\w\d\s]', ' ', s)
        norm = re.sub(r'\s+', ' ', norm)
        return norm.strip()
