import re
import datetime

from django.conf import settings
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponse, \
    HttpResponseForbidden, \
    HttpResponseBadRequest, \
    HttpResponseNotFound, \
    JsonResponse


from .models import PasswordRecovery
# from .forms import AuthenticationForm, CaptchaForm


# @permission_required('polls.can_vote', login_url='/loginpage/')
@login_required(login_url='/accounts/login/')
def custom_dashboard(request):
    context = dict()
    return render(request, 'home.html', context)


@sensitive_post_parameters()
@csrf_protect
def custom_login(request):
    context = dict()
    response = dict(Status="UNKNOWN", Error=[], FieldErrors=[])
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        remember_me = request.POST.get('remember_me', False)
        # auth_form = AuthenticationForm(request.POST)
        if auth_form.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)
                    response["Status"] = "OK"
                    return JsonResponse(response, **{'status': 200})
                else:
                    response["Status"] = "FAILED"
                    response["Error"].append('Sorry! this account is disabled or not active yet')
                    return JsonResponse(response, **{'status': 403})
            response["Status"] = "FAILED"
            response["Error"].append('Invalid credentials, either username/password is incorrect, please try again!')
            return JsonResponse(response, **{'status': 404})
        else:
            response["Status"] = "FAILED"
            response["FieldErrors"] = auth_form.errors
            return JsonResponse(response, **{'status': 400})

    else:
        form = CaptchaForm()
        # context['form'] = form
        context['form'] = ""

    return render(request, 'login.html', context)


@sensitive_post_parameters()
@csrf_protect
def change_password(request, secret_key):
    context = dict()
    try:
        recovery_obj = PasswordRecovery.objects.get(secret_key=secret_key)
        user = recovery_obj.user
        context['user'] = user
        context['secret_key'] = secret_key

        now = datetime.datetime.now()
        time_left = recovery_obj.last_modified + datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        time_left = time_left.replace(tzinfo=None)
        if time_left <= now:
            context['message'] = 'Forbidden! Your password change request activation link has been expired. '
            return render(request, 'error_pages/default.html', context)

        if request.method == "POST":
            status = 400
            response = dict(Status="UNKNOWN", Error=[], FieldErrors=[])

            password1 = request.POST.get("password1", None)
            password2 = request.POST.get("password2", None)

            if len(password1) == 0 or password1 == "" or password1 == " " or password1 is None:
                response["Status"] = "FAILED"
                response["FieldErrors"] = {"password1": ["This field is required"]}
            elif len(password2) == 0 or password2 == "" or password2 == " " or password2 is None:
                response["Status"] = "FAILED"
                response["FieldErrors"] = {"password2": ["This field is required"]}
            elif password2 != password1:
                response["Status"] = "FAILED"
                response["FieldErrors"] = {"password2": ["Password does not match"]}
            elif len(password2) < 8:
                response["Status"] = "FAILED"
                response["FieldErrors"] = {"password1": ["Please note, your password should have at least 8 characters"]}
            elif user.check_password(password2):
                response["Status"] = "FAILED"
                response["FieldErrors"] = {"password1": ["Password is too similar with old password, please try again"]}
            elif not re.match(r"^((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).{8,20})$", password2):
                response["Status"] = "FAILED"
                response["FieldErrors"] = {"password1": ["Please note, your password must have "
                                                         "uppercase and lowercase letters, special "
                                                         "characters and numbers"]}
            else:
                status = 200
                user.set_password(password2)
                user.save()
                response["Status"] = "Success"

            return JsonResponse(response, **{'status': status})

    except PasswordRecovery.DoesNotExist:
        context['message'] = 'Oops! Invalid password change request. '
        return render(request, 'error_pages/default.html', context)

    return render(request, 'accounts/change_password.html', context)


@login_required(login_url='/accounts/login/')
def profile_about(request):
    context = dict()
    return render(request, 'profile-about.html', context)
