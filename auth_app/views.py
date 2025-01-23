from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .models import Role, Customer
from .serializers import (
    RoleSerializer, UserCreateSerializer, UserUpdateSerializer,
    LoginSerializer, ChangePasswordSerializer, CustomerSerializer
)
from .permissions import IsAdminOrSuperUser

User = get_user_model()

class LoginView(APIView):
    permission_classes = []  # Allow unauthenticated access

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'accessToken': str(refresh.access_token),
                    'refreshToken': str(refresh),
                    'userType': user.role.name
                })
            
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

    def destroy(self, request, *args, **kwargs):
        role = self.get_object()
        if User.objects.filter(role=role).exists():
            return Response(
                {"error": "Cannot delete role as it is assigned to users"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserUpdateSerializer

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"error": "Wrong old password"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"status": "password changed successfully"})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response({
            "status": f"User {'activated' if user.is_active else 'deactivated'} successfully"
        })

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = []
    lookup_field = 'mobile_number'

    def create(self, request, *args, **kwargs):
        mobile_number = request.data.get('mobile_number')
        customer, created = Customer.objects.get_or_create(
            mobile_number=mobile_number
        )
        serializer = self.get_serializer(customer)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )




# import random
# import json

# from django.conf import settings
# from django.http import JsonResponse
# from django.views import View
# from twilio.rest import Client
# from .models import CustomUser
# from django.contrib.auth import login
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.contrib.auth import authenticate, login
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import UserRegistrationSerializer, UserLoginSerializer

# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             # Authenticate using the provided username and password
#             user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
#             if user is not None:
#                 login(request, user)
#                 return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
#             return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @method_decorator(csrf_exempt, name='dispatch')
# class SendOTPView(View):
#     def post(self, request):
#         if request.content_type == 'application/json':
#             try:
#                 data = json.loads(request.body)
#                 phone_number = data.get('phone_number')
#             except json.JSONDecodeError:
#                 return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
#         else:
#             # Assume form-encoded data
#             phone_number = request.POST.get('phone_number')     
#         if not phone_number:
#             return JsonResponse({'error': 'Phone number is required.'}, status=400)

#         # Retrieve or create user with the given phone number
#         user, created = CustomUser.objects.get_or_create(phone_number=phone_number)
#         # Generate a random OTP and save it in the user's otp_code field
#         otp_code = str(random.randint(100000, 999999))
#         user.otp_code = otp_code
#         user.save()

#         # Send OTP via Twilio
#         client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#         try:
#             message = client.messages.create(
#                 body=f'Your OTP is: {otp_code}',
#                 from_=settings.TWILIO_PHONE_NUMBER,
#                 to=phone_number
#             )
#             return JsonResponse({'message': 'OTP sent successfully.'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

# @method_decorator(csrf_exempt, name='dispatch')
# class ResendOTPView(View):
#     def post(self, request):
#         # Handle JSON and form-encoded data
#         if request.content_type == 'application/json':
#             try:
#                 data = json.loads(request.body)
#                 phone_number = data.get('phone_number')
#             except json.JSONDecodeError:
#                 return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
#         else:
#             phone_number = request.POST.get('phone_number')     

#         if not phone_number:
#             return JsonResponse({'error': 'Phone number is required.'}, status=400)

#         # Retrieve or create user with the given phone number
#         user, created = CustomUser.objects.get_or_create(phone_number=phone_number)

#         # Generate a random OTP
#         otp_code = str(random.randint(100000, 999999))

#         # Update the user's OTP code (ensure to save it in a model)
#         user.otp_code = otp_code
#         user.save()

#         # Send OTP via Twilio
#         client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#         try:
#             message = client.messages.create(
#                 body=f'Your OTP is: {otp_code}',
#                 from_=settings.TWILIO_PHONE_NUMBER,
#                 to=phone_number
#             )
#             return JsonResponse({'message': 'OTP sent successfully.'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)


# @method_decorator(csrf_exempt, name='dispatch')
# class VerifyOTPView(View):
#     def post(self, request):
#         if request.content_type == 'application/json':
#             try:
#                 data = json.loads(request.body)
#                 phone_number = data.get('phone_number')
#                 otp_code = data.get('otp_code')
#             except json.JSONDecodeError:
#                 return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
#         else:
#             # Assume form-encoded data
#             phone_number = request.POST.get('phone_number')
#             otp_code = request.POST.get('otp_code')

#         # Validate both fields
#         if not phone_number or not otp_code:
#             return JsonResponse({'error': 'Phone number and OTP are required.'}, status=400)

#         # Authenticate the user
#         try:
#             user = CustomUser.objects.get(phone_number=phone_number, otp_code=otp_code)
#             # If OTP is valid, log the user in and clear the OTP field
#             login(request, user)
#             user.otp_code = None  # Clear OTP after successful login
#             user.save()
#             return JsonResponse({'message': 'Login successful.'})
#         except CustomUser.DoesNotExist:
#             return JsonResponse({'error': 'Invalid phone number or OTP.'}, status=400)
