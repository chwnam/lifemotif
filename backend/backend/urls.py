"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from .views import (
    PythonSocialAuthComplete,
    PythonSocialAuthLoginError,
    index,
    ApiEndpoint,
)

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    # prototype index
    url(r'^$', index, name='index'),

    # Django Admin
    url(r'^admin/', admin.site.urls),

    # emails app
    url(r'', include('emails.urls', namespace='emails')),

    # users app
    url(r'', include('users.urls', namespace='users')),

    # OAuth login error, and successful views
    url(r'^login-error/$', PythonSocialAuthLoginError.as_view()),

    url(r'^complete/(?P<backend>[^/]+)/$', PythonSocialAuthComplete.as_view()),

    # Django REST framework api_v1 auth
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Python social apps URL
    url(r'', include('social.apps.django_app.urls', namespace='social')),

    # Django OAuth Toolkit
    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    url(r'^api/hello', csrf_exempt(ApiEndpoint.as_view())),
]
