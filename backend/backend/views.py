from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from social.apps.django_app.views import complete
from social.exceptions import AuthFailed, AuthAlreadyAssociated


class PythonSocialAuthComplete(View):
    @staticmethod
    def get(request, *args, **kwargs):
        backend = kwargs.pop('backend')
        try:
            return complete(request, backend, *args, **kwargs)
        except AuthFailed:
            return HttpResponseRedirect(reverse('login'))
        except AuthAlreadyAssociated:
            return HttpResponseRedirect(reverse('login'))


class PythonSocialAuthLoginError(View):
    @staticmethod
    def get(request):
        return HttpResponse(status=401)


def index(request):
    """
    Simple index logic
    :param request:
    :return:
    """
    return render(request, 'index.html', {'user': request.user})


from django.http.response import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView
class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, Oauth2!')
    def post(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2, by POST method!!')
