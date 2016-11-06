from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/v1/gmail/', include('emails.api.v1.gmail.urls', namespace='emails-api-v1')),
]
