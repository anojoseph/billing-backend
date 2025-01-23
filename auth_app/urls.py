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


# from django.urls import path
# from .views import *

# urlpatterns = [

#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('send-otp/', SendOTPView.as_view(), name='send_otp'),
#     path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),

#     path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
# ]
