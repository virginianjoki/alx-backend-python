# chats/middleware.py

import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.http import HttpResponseTooManyRequests


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Format: {ip: [list of timestamps]}
        self.request_log = {}

    def __call__(self, request):
        if request.method == 'POST' and '/chat/' in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Remove timestamps older than 1 minute
            timestamps = self.request_log.get(ip, [])
            timestamps = [ts for ts in timestamps if now -
                          ts < timedelta(minutes=1)]

            if len(timestamps) >= 5:
                return HttpResponseTooManyRequests("Rate limit exceeded: max 5 messages per minute.")

            # Add current timestamp
            timestamps.append(now)
            self.request_log[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        """ Get client IP address even if behind proxy """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


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
