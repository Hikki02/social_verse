from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class ProductPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

    def get_paginated_response(self, data):
        """Override the method to customize the paginated response."""
        return Response({
            'count': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
