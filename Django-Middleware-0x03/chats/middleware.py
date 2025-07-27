# chats/middleware.py

import logging
from datetime import datetime
from django.http import HttpResponseForbidden


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()

        # Access is allowed only between 6:00 PM and 9:00 PM
        from datetime import time
        start = time(18, 0)  # 6:00 PM
        end = time(21, 0)    # 9:00 PM

        if not (start <= now <= end):
            return HttpResponseForbidden("Chat access is only allowed between 6:00 PM and 9:00 PM.")

        return self.get_response(request)


# Configure the logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_entry)
        response = self.get_response(request)
        return response
