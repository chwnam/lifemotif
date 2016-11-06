from django.conf.urls import include, url
from django.contrib.auth.views import login, logout, login_required

from . import views

urlpatterns = [
    url(r'^api/v1/', include('users.api.v1.urls', namespace='users_api_v1')),

    # login
    url(
        r'^users/login',
        login,
        kwargs={
            'template_name': 'users/login.html'
        },
        name='login'
    ),

    # logout
    url(
        r'^users/logout',
        logout,
        kwargs={
            'template_name': 'users/logout.html'
        },
        name='logout'
    ),

    # profile
    url(
        r'^users/profile/?$',
        login_required(views.UserProfile.as_view()),
        name='profile'
    ),
]
