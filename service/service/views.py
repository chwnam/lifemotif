from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from social.apps.django_app.views import complete
from social.exceptions import AuthFailed, AuthAlreadyAssociated


class AuthComplete(View):
    def get(self, request, *args, **kwargs):
        backend = kwargs.pop('backend')
        try:
            return complete(request, backend, *args, **kwargs)
        except AuthFailed:
            return HttpResponseRedirect(reverse('login'))
        except AuthAlreadyAssociated:
            return HttpResponseRedirect(reverse('login'))


class LoginError(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=401)
