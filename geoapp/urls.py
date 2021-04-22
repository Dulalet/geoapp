"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from rest_framework.authtoken.views import obtain_auth_token

# from geo.views import GetLayer, UpdateLayer
from geo.views import get_layer
from geoapp import settings

schema_view = get_swagger_view(title='geoapp')

urlpatterns = [
    path('', schema_view),
    path('admin/', admin.site.urls),
    path('geo/', include('geo.urls')),
    path('', include('users.urls')),

    path('getLayers/', get_layer, name="layers"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)