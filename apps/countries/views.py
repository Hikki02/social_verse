from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from services.base.pagination import ProductPagination
from .serializers import CountrySerializer, CountryDetailSerializer
from .services.country import CountryService, ListCountryService, RetrieveCountryService


class CountryViewSet(viewsets.ViewSet, viewsets.GenericViewSet):
    """
    ViewSet для работы со странами.
    """
    permission_classes = [AllowAny]
    serializer_class = CountrySerializer
    pagination_class = ProductPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        list_service = ListCountryService()
        retrieve_service = RetrieveCountryService()
        self.country_service = CountryService(list_service, retrieve_service)

    def get_serializer_class(self):
        """
        Определяет сериалайзер для действий 'list' и 'retrieve'.
        """
        serializer_map = {
            'list': CountrySerializer,
            'retrieve': CountryDetailSerializer,
        }
        return serializer_map.get(self.action, self.serializer_class)

    @swagger_auto_schema(
        responses={200: CountrySerializer(many=True)},
        operation_description="Получить список стран, у которых есть хотя бы один пост."
    )
    def list(self, request):
        """
        Получить список стран, у которых есть хотя бы один пост.
        """
        countries = self.country_service.list_countries_with_posts()
        paginator = self.pagination_class()  # Инициализируем пагинатор
        paginated_countries = paginator.paginate_queryset(countries, request)
        serializer = self.get_serializer(paginated_countries, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        responses={200: CountryDetailSerializer()},
        operation_description="Получить информацию о конкретной стране.",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="ID страны", type=openapi.TYPE_INTEGER),
        ]
    )
    def retrieve(self, request, pk=None):
        """
        Получить информацию о конкретной стране.
        """
        country_data = self.country_service.retrieve_country(pk)

        country = country_data['country']
        additional_data = country_data['country_data']

        serializer = self.get_serializer(country)
        response_data = serializer.data
        response_data.update({'country_data': additional_data})
        return Response(response_data, status=status.HTTP_200_OK)
