from rest_framework import routers
from django.urls import path
from .views import AuthViewSet

# router = routers.DefaultRouter(trailing_slash=False)
# router.register('api/auth', AuthViewSet, basename='auth')
#
# urlpatterns = router.urls

urlpatterns = [
    # Request
    # {
    #     "email": "hello@example.com",
    #     "password": "VerySafePassword0909"
    # }
    path('login/', AuthViewSet.as_view({'post': 'login'})),
    # Request
    # {
    #     "email": "hello@example.com",
    #     "password": "VerySafePassword0909",
    #     "first_name": "John",
    #     "last_name": "Howley",
    # }
    path('register/', AuthViewSet.as_view({'post': 'register'})),
    path('logout/', AuthViewSet.as_view({'post': 'logout'})),
    path('getUser/', AuthViewSet.as_view({'get': 'get_user'})),
    path('password_change/', AuthViewSet.as_view({'post': 'password_change'})),
]



# from django.urls import path, include
# from .views import RegisterAPI, LoginAPI, UserAPI
# from knox import views as knox_views
#
#
# urlpatterns = [
#   # path('api/auth/', include('knox.urls')),
#   path('api/auth/register/', RegisterAPI.as_view()),
#   path('api/auth/login/', LoginAPI.as_view()),
#   # path('api/auth/login/', login),
#   path('api/auth/user/', UserAPI.as_view()),
#   path('api/auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout')
# ]