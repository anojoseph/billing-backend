from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Role, Customer

User = get_user_model()

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['created_at']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'confirm_password', 'role', 
                 'first_name', 'last_name', 'email', 'is_active']
        read_only_fields = ['id']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'first_name', 'last_name', 
                 'email', 'is_active']
        read_only_fields = ['id']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("New passwords do not match")
        return data

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'mobile_number', 'created_at']
        read_only_fields = ['created_at']




# # auth_app/serializers.py

# from rest_framework import serializers
# from .models import CustomUser, Role

# class RoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = ['id', 'name']  # Include id in the serialized output


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'phone_number', 'password', 'role']

#     def create(self, validated_data):
#         user = CustomUser(
#             username=validated_data['username'],
#             phone_number=validated_data.get('phone_number'),  # This will be used for OTP if provided
#             role=validated_data.get('role')  # Set role if provided
#         )
#         user.set_password(validated_data['password'])  # Set hashed password
#         user.save()
#         return user
    
# class UserLoginSerializer(serializers.Serializer):
#     username = serializers.CharField()  # This can be either the phone number or the provided username
#     password = serializers.CharField(write_only=True)