from django.conf.urls import url

from . import api_views

urlpatterns = [
    url(r'^tid-index/?$', api_views.TidIndexView.as_view()),
    url(r'^tid-index/(?P<pk>\d+)', api_views.TidIndexDetailView.as_view()),

    url(r'^mid-index/?$', api_views.MidIndexView.as_view()),
    url(r'^mid-index/(?P<pk>\d+)', api_views.MidIndexDetailView.as_view()),

    url(r'^profiles/?$', api_views.ProfilesView.as_view()),
    url(r'^profiles/(?P<pk>\d+)', api_views.ProfileDetailView.as_view()),

    # /api/v1/gmail/labels: list the email account's labels (a.k.a. mailboxes)
    url(r'^labels/?$', api_views.LabelsView.as_view()),

    url(r'^update-index/(?P<profile_id>\d+)', api_views.UpdateIndexView.as_view()),

    # url(r'^reset-index/(?P<profile_id>\d+)', api_views.ResetIndexView.as_view()),
]
