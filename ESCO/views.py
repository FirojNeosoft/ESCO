import logging, string, random

from django.views import View
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.decorators import method_decorator

from ESCO.decorators import *
from CMS.models import *

logger = logging.getLogger('tracker_log')


class LoginView(View):
    """
    Login view
    """
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            logger.error('wrong credentials for user {}'.format(request.POST['username']))
            messages.error(request, 'Please check credentials.')
            return HttpResponseRedirect('')
        elif user is not None and settings.TWO_FACTOR_AUTHENTICATION == False:
            login(request, user)
            return HttpResponseRedirect(reverse('list_surveys'))
        elif user is not None and settings.TWO_FACTOR_AUTHENTICATION:
            obj, created = UserVerification.objects.get_or_create(user=user)
            obj.otp = int(''.join([random.choice(string.digits) for n in range(4)]))
            obj.save()
            send_mail(
                'ECPG: OTP Generated',
                'Hi ' + user.username + ',\n Your credentials are correct. Proceed your authentication process by using the OTP number ' + str(obj.otp)+'\n\nThanks And Regards,\nECPG Team.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return render(request, 'otp_verification.html', {'username': user.username})


class UserVerificationView(View):
    """
    User verification view
    """
    def post(self, request):
        user = User.objects.get(username=request.POST['username'])
        otp = UserVerification.objects.get(user=user).otp
        if int(request.POST['otp']) == otp:
            login(request, user)
            return HttpResponseRedirect(reverse('list_surveys'))
        else:
            logger.error('Invalid OTP For user {}'.format(request.POST['username']))
            messages.error(request, 'Invalid OTP.')
            return render(request, 'otp_verification.html', {'username': user.username})


@method_decorator(check_validity_of_license, name='dispatch')
class LogoutView(LoginRequiredMixin, View):
    """
    Logout view
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('sys_login'))


@method_decorator(check_validity_of_license, name='dispatch')
class ChangePasswordView(LoginRequiredMixin, View):
    """
    Change Password
    """
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:
            logger.error('Failed to change password by user {}'.format(request.user.username))
            messages.error(request, 'Error occured while changing password, please enter a proper password.')
        return redirect('change_password')

