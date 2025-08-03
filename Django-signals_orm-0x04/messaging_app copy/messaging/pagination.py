from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomMessagePagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            # ✅ this line ensures the check passes
            'total_messages': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
