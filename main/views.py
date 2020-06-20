from django.shortcuts import render
from django.contrib.auth import logout
from kalenda.utils.google_token import check_google_token
from allauth.socialaccount.models import SocialToken


def home(request):
    user = request.user
    context = {}
    return render(request, 'kalenda/index.html', context=context)