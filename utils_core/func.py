from functools import wraps
import signal

from utils_core import plural


def timeout(seconds, message=None):
    """ Decorator to timeout a function

    :param int seconds: Seconds to wait before timeout happens (raises TimeoutError)
    :param str message: The message for TimeoutError
    """
    if not message:
        message = f'Timed out after {seconds} ' + plural('second', seconds)

    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(message)

        @wraps(func)
        def decorated(*args, **kwargs):
            old_handler = signal.signal(signal.SIGALRM, _handle_timeout)
            old_alarm = signal.alarm(seconds)

            try:
                return func(*args, **kwargs)

            finally:
                signal.alarm(old_alarm)
                signal.signal(signal.SIGALRM, old_handler)

        return decorated

    return decorator
