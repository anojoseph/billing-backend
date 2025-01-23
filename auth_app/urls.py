from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, RoleViewSet, UserViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
