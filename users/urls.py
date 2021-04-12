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
    # path('password_change/', AuthViewSet.as_view({'post': 'password_change'})),
]
