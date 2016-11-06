from django.shortcuts import render
from django.views.generic import View


class UserProfile(View):
    @staticmethod
    def get(request):
        return render(request, 'users/profile.html', {'user': request.user})

    @staticmethod
    def post(request):
        password = request.POST.get('password')
        if password and request.user.is_authenticated:
            request.user.set_password(password)
            request.user.save()
        return render(request, 'users/profile.html', {'user': request.user})
