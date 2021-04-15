from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .utils import get_and_authenticate_user, create_user_account

User = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'register': serializers.UserRegisterSerializer,
        'password_change': serializers.PasswordChangeSerializer,
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()



# from django.contrib.auth.models import User
# from rest_framework import generics, permissions
# from rest_framework.decorators import permission_classes, api_view
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from knox.models import AuthToken
# from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
#
# # Register API
# from .utils import create_user_account
#
#
# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = RegisterSerializer
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # user = create_user_account(**serializer.validated_data)
#         # data = AuthUserSerializer(user).data
#         # return Response(data=data, status=status.HTTP_201_CREATED)
#         #
#         # serializer = self.get_serializer(data=request.data)
#         # serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#             "user": UserSerializer(user, context=self.get_serializer_context()).data,
#             "token": AuthToken.objects.create(user)[1]
#         })
#
#
# # Login API
#
# class LoginAPI(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data
#         cond, token = AuthToken.objects.get_or_create(user=user)
#         print('1', cond)
#         print('2', token)
#
#         return Response({
#             "user": UserSerializer(user, context=self.get_serializer_context()).data,
#             "token": token
#         })
# # @api_view(["POST"])
# # @permission_classes((AllowAny,))
# # def login(request):
# #     serializer = LoginSerializer(data=request.data)
# #     serializer.is_valid(raise_exception=True)
# #     user = serializer.validated_data
# #     cond, token = AuthToken.objects.get_or_create(user=user)
# #     print('1', cond)
# #     print('2', token)
# #
# #     return Response({
# #         "user": UserSerializer(user, context=self.get_serializer_context()).data,
# #         "token": token
# #     })
#
#
# # Get User API
# class UserAPI(generics.RetrieveAPIView):
#     permission_classes = [
#         permissions.IsAuthenticated,
#     ]
#     serializer_class = UserSerializer
#
#     def get_object(self):
#         return self.request.user
