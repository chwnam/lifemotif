from django.conf.urls import url

from . import api_views

urlpatterns = [
    # list users, or create a new email profile
    url(r'^users/?$', api_views.UsersView.as_view(), name='users'),

    # get a user by pk
    url(r'^users/(?P<pk>\d+)/?$', api_views.UsersDetailView.as_view(), name='users_detail'),
]
