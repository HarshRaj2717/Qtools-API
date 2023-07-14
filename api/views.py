from django.shortcuts import render
from django.http import JsonResponse
from random import randint
from .models import Users
from . import helpers

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register_user(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    verification_code = request.GET.get('code')

    # In case an verification_code is provided
    if verification_code != None:
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
            elif cur_user_status == 1 or cur_user_status == 2:
                if cur_user.match_verification_code(verification_code) or cur_user_status == 2:
                    return JsonResponse({
                        'success': 1,
                        'message': 'Account Verified.',
                        'redirect': '/#tools',
                        'api_token': cur_user.api_token,
                    })
                else:
                    return JsonResponse({
                        'success': 0,
                        'message': 'Incorrect verification code entered!',
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

    # Checking if both email & password not are given
    if email == None or email.strip() == "" or password == None or password.strip() == "":
        return JsonResponse({
            'success': 0,
            'message': 'Please provide both email & password.',
            'redirect': None,
        })

    # Checking if both email & password aren't very long in length
    if len(email.strip()) > 100 or len(password.strip()) > 20:
        return JsonResponse({
            'success': 0,
            'message': 'Too long email or password.',
            'redirect': None,
        })

    password = helpers.generate_hash(password)
    api_token = helpers.generate_hash(
        str(email + password + str(randint(1, 20))))

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
                'success': 1,
                'message': 'Verification Code Sent.',
                'redirect': '/verify',
            })
        elif cur_user_status == 2:
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

    if cur_user.send_verification_code():
        cur_user.save()
        return JsonResponse({
            'success': 1,
            'message': 'Verification Code Sent.',
            'redirect': '/verify',
        })
    else:
        return JsonResponse({
            'success': 0,
            'message': 'Unknown Exception Occurred! Please contact Harsh Raj (harshraj2717@gmail.com).',
            'redirect': None,
        })


def login_user(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    verification_code = request.GET.get('code')

    # In case an verification_code is provided
    if verification_code != None:
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
            elif cur_user_status == 1 or cur_user_status == 2:
                if cur_user.match_verification_code(verification_code) or cur_user_status == 2:
                    return JsonResponse({
                        'success': 1,
                        'message': 'Account Verified.',
                        'redirect': '/#tools',
                        'api_token': cur_user.api_token,
                    })
                else:
                    return JsonResponse({
                        'success': 0,
                        'message': 'Incorrect verification code entered!',
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

    # Checking if both email & password are not given
    if email == None or email.strip() == "" or password == None or password.strip() == "":
        return JsonResponse({
            'success': 0,
            'message': 'Please provide both email & password.',
            'redirect': None,
        })

    # Checking if both email & password aren't very long in length
    if len(email.strip()) > 100 or len(password.strip()) > 20:
        return JsonResponse({
            'success': 0,
            'message': 'Too long email or password.',
            'redirect': None,
        })

    password = helpers.generate_hash(password)

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
                'message': 'User not verified.',
                'redirect': '/verify',
            })
        elif cur_user_status == 2:
            if cur_user.password == password:
                return JsonResponse({
                    'success': 1,
                    'message': 'Logged in.',
                    'redirect': '/#tools',
                    'api_token': cur_user.api_token,
                })
            else:
                return JsonResponse({
                    'success': 0,
                    'message': 'Incorrect password.',
                    'redirect': None,
                })
        else:
            return JsonResponse({
                'success': 0,
                'message': 'Unknown Exception Occurred! Please contact Harsh Raj (harshraj2717@gmail.com).',
                'redirect': None,
            })
    except:
        return JsonResponse({
            'success': 0,
            'message': 'User doesn\'t exists.',
            'redirect': '/register',
        })
