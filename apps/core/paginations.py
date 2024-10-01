from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # Общее количество объектов
            'page_count': self.page.paginator.num_pages,  # Общее количество страниц
            'current_page': self.page.number,  # Текущая страница
            'items_per_page': self.page_size,  # Количество объектов на странице
            'results': data  # Данные текущей страницы
        })
