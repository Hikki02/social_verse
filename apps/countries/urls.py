from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='countries')

urlpatterns = [
    path('countries/with-posts/', CountryViewSet.as_view({'get': 'list'}), name='country-list-with-posts'),
    path('countries/<int:pk>/', CountryViewSet.as_view({'get': 'retrieve'}), name='country-detail'),

]

urlpatterns += router.urls
