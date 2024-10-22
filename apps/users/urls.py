from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SubscriptionViewSet

# Создайте экземпляр маршрутизатора
router = DefaultRouter()
# Регистрация вашего UserViewSet
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('users/sign_up/', UserViewSet.as_view({'post': 'sign_up'}), name='user-sign-up'),  # Регистрация пользователя
    path('users/sign_in/', UserViewSet.as_view({'post': 'sign_in'}), name='user-sign-in'),  # Вход пользователя
    path('users/', UserViewSet.as_view({'get': 'list'}), name='user-list'),  # Получить список всех пользователей

    path('subscriptions/subscribe/user/<int:pk>/', SubscriptionViewSet.as_view({'post': 'subscribe_to_user'}), name='subscribe-to-user'),
    path('subscriptions/unsubscribe/user/<int:pk>/', SubscriptionViewSet.as_view({'post': 'unsubscribe_from_user'}), name='unsubscribe-from-user'),
    path('subscriptions/subscribe/country/<int:country_id>/', SubscriptionViewSet.as_view({'post': 'subscribe_to_country'}), name='subscribe-to-country'),
    path('subscriptions/unsubscribe/country/<int:country_id>/', SubscriptionViewSet.as_view({'post': 'unsubscribe_from_country'}), name='unsubscribe-from-country'),
    path('subscriptions/subscribe/tag/<int:tag_id>/', SubscriptionViewSet.as_view({'post': 'subscribe_to_tag'}), name='subscribe-to-tag'),
    path('subscriptions/unsubscribe/tag/<int:tag_id>/', SubscriptionViewSet.as_view({'post': 'unsubscribe_from_tag'}), name='unsubscribe-from-tag'),

]

# Добавьте маршрутизатор в urlpatterns
urlpatterns += router.urls
