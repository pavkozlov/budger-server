
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
