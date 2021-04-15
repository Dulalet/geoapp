from django.contrib.auth import get_user_model, password_validation
from rest_framework.authtoken.models import Token
from rest_framework import serializers

from django.contrib.auth.models import BaseUserManager

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'auth_token')
        read_only_fields = ('id', 'is_active', 'is_staff')

    def get_auth_token(self, obj):
        token, cond = Token.objects.get_or_create(user=obj)
        return token.key


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class EmptySerializer(serializers.Serializer):
    pass



# from rest_framework import serializers
# from django.contrib.auth.models import User, BaseUserManager
# from django.contrib.auth import authenticate, password_validation
#
#
# # User Serializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email')
#
#
# # Register Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField()
#     # username = serializers.CharField(max_length=25, required=False)
#     username = serializers.SerializerMethodField(required=False)
#     password = serializers.CharField(max_length=25)
#     first_name = serializers.CharField(max_length=25, required=False)
#     last_name = serializers.CharField(max_length=25, required=False)
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
#         # fields = ('id', 'email', 'password', 'first_name', 'last_name')
#         # fields = ('id', 'username', 'email', 'password')
#         extra_kwargs = {'password': {'write_only': True}}
#
#         def get_username(self, obj):
#             return obj.email
#
#         def validate_email(self, value):
#             user = User.objects.filter(email=value)
#             if user:
#                 raise serializers.ValidationError("Email is already taken")
#             return BaseUserManager.normalize_email(value)
#
#         def validate_password(self, value):
#             password_validation.validate_password(value)
#             return value
#
#         def create(self, validated_data):
#             print('test')
#             print(validated_data['username'])
#             user = User.objects.create_user(username=validated_data['email'], email=validated_data['email'],
#                                             password=validated_data['password'],
#                                             first_name=validated_data['first_name'],
#                                             last_name=validated_data['last_name'])
#
#             return user
#
#
# # Login Serializer
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#
#     def validate(self, data):
#         user = authenticate(**data)
#         if user and user.is_active:
#             return user
#         raise serializers.ValidationError("Incorrect Credentials")
