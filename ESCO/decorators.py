from datetime import datetime as dt

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect


def check_validity_of_license(function):
    def wrap(request, *args, **kwargs):
        if dt.today().date() > dt.strptime(settings.APP_LICENSE_EXPIRY_DATE, '%m/%d/%Y').date():
            messages.error(request, 'Your application is expired. Please contact your developers.')
            return redirect('sys_login')
        else:
            return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    return wrap
