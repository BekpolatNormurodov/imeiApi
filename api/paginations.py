from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'
    max_page_size = 100
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'total_records': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link() is not None,
            'previous': self.get_previous_link() is not None,
            'next_id': self.page.next_page_number() if self.page.has_next() else None,
            'previous_id': self.page.previous_page_number() if self.page.has_previous() else None,
            'data': data,
        })
