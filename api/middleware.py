import threading

# Thread-local storage to hold the user
_user = threading.local()


def get_current_user():
    return getattr(_user, 'value', None)


class RequestUserMiddleware:
    """Middleware to add the request user to thread-local storage."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user  # Save the current user in thread-local storage
        response = self.get_response(request)
        return response
