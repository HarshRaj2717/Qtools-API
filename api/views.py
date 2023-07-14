from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Users
from . import helpers

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register_user(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    otp = request.GET.get('otp')

    # In case an OTP is provided
    if otp != None:
        try:
            # Checking user status in existing database
            cur_user = Users.objects.get(email)
            cur_user_status = cur_user.user_status()
            if cur_user_status == 0:
                return JsonResponse({
                    'success': 0,
                    'message': 'Sorry, the user has been blocked or deleted.',
                    'redirect': None,
                })
            elif cur_user_status == 1:
                if cur_user.match_otp(otp):
                    return JsonResponse({
                        'success': 1,
                        'message': 'Account Verified.',
                        'redirect': '/#tools',
                    })
                else:
                    return JsonResponse({
                        'success': 0,
                        'message': 'Incorrect OTP entered!',
                        'redirect': None,
                    })
            else:
                return JsonResponse({
                    'success': 0,
                    'message': 'Unknown Exception Occurred! Please contact Harsh Raj (harshraj2717@gmail.com).',
                    'redirect': None,
                })
        except Users.DoesNotExist:
            return JsonResponse({
                'success': 0,
                'message': 'Unknown Exception Occurred! Please contact Harsh Raj (harshraj2717@gmail.com).',
                'redirect': None,
            })

    # Checking if both email & password are given
    if email == None or email.strip() == "" or password == None or password.strip() == "":
        return JsonResponse({
            'success': 0,
            'message': 'Please provide both email & password.',
            'redirect': None,
        })

    password = helpers.generate_hash(password)
    api_token = helpers.generate_hash(str(email + password))

    try:
        # Checking user status in existing database
        cur_user = Users.objects.get(email=email)
        cur_user_status = cur_user.user_status()
        if cur_user_status == 0:
            return JsonResponse({
                'success': 0,
                'message': 'Sorry, the user has been blocked or deleted.',
                'redirect': None,
            })
        elif cur_user_status == 1:
            return JsonResponse({
                'success': 0,
                'message': 'User already exists! Please Login.',
                'redirect': '/login',
            })
        else:
            return JsonResponse({
                'success': 0,
                'message': 'Unknown Exception Occurred! Please contact Harsh Raj (harshraj2717@gmail.com).',
                'redirect': None,
            })
    except Users.DoesNotExist:
        cur_user = Users(
            email=email,
            password=password,
            api_token=api_token
        )

    if cur_user.is_email_disposable():
        return JsonResponse({
            'success': 0,
            'message': 'Disposable email detected. Please use a different mailing id.',
            'redirect': None,
        })

    if cur_user.send_otp():
        cur_user.save()
        return JsonResponse({
            'success': 1,
            'message': 'OTP Sent for verification.',
            'redirect': '/verify',
        })
    else:
        return JsonResponse({
            'success': 0,
            'message': 'Unknown Exception Occurred! Please contact Harsh Raj (harshraj2717@gmail.com).',
            'redirect': None,
        })


def login_user(request):
    '''
    TODO
    '''
    ...


def forgot_password(request):
    '''
    TODO
    '''
    ...
