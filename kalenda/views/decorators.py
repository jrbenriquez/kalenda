from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, reverse
from django.contrib.auth import logout
from django.utils import timezone
from kalenda.utils.google_token import check_google_account


def attach_google_token(func):
    # This checks if there is a google account registered for the user and attached the token to the request.
    # Token automatically refreshes if expired using the stored refresh token
    def _attach_google_token(request, *args, **kwargs):
        user = request.user
        social_account = user.socialaccount_set.filter(provider='google')
        if social_account:
            account = social_account.last()

            account = check_google_account(account)
            google_token_object = account.socialtoken_set.first()

            google_access_token = google_token_object.token

            request.google_token = google_access_token
        else:
            logout(request)
            return redirect(reverse('home'))
        try:
            return func(request, *args, **kwargs)
        except PermissionDenied as e:
            logout(request)
            return redirect(reverse('home'))
    return _attach_google_token
