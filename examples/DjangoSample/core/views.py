from error_tracker.django.middleware import error_tracker


def error(request):
    raise ValueError("Just some test")


def die(request):
    try:
        raise ValueError("Another test")
    except Exception as e:
        error_tracker.record_exception(request, e)
        raise e
