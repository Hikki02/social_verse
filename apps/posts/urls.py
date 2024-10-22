from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, DashboardViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list'),  # Получить все посты или создать новый
    path('posts/<int:pk>/', PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='post-detail'),  # Получить, обновить или удалить пост
    path('home_page/', PostViewSet.as_view({'get': 'main_page'}), name='home-page'),  # Главная страница

    path('dashboard/', DashboardViewSet.as_view({'get': 'list'}), name='dashboard-list'),  # Получить данные для блока с постами, тегами и топ пользователями
]

urlpatterns += router.urls
