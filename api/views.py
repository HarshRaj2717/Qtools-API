from django.shortcuts import render
from django.http import JsonResponse
from random import randint
from .models import Users
from . import helpers

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register_user(request):
    EMAIL = request.GET.get('email')
    PASSWORD = request.GET.get('password')
    VERIFICATION_CODE = request.GET.get('code')

    # In case an verification_code is provided
    if VERIFICATION_CODE != None:
        try:
            # Checking user status in existing database
            cur_user = Users.objects.get(email=EMAIL)
            cur_user_status = cur_user.user_status()
            if cur_user_status == 0:
                return JsonResponse({
                    'success': 0,
                    'message': 'Sorry, the user has been blocked or deleted.',
                    'redirect': None,
                })
            elif cur_user_status == 1 or cur_user_status == 2:
                if cur_user.match_verification_code(VERIFICATION_CODE) or cur_user_status == 2:
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
    if EMAIL == None or EMAIL.strip() == "" or PASSWORD == None or PASSWORD.strip() == "":
        return JsonResponse({
            'success': 0,
            'message': 'Please provide both email & password.',
            'redirect': None,
        })

    PASSWORD = helpers.generate_hash(PASSWORD)
    api_token = helpers.generate_hash(
        str(EMAIL + PASSWORD + str(randint(1, 20))))

    try:
        # Checking user status in existing database
        cur_user = Users.objects.get(email=EMAIL)
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
            email=EMAIL,
            password=PASSWORD,
            api_token=api_token
        )

    if cur_user.is_email_disposable():
        return JsonResponse({
            'success': 0,
            'message': 'Disposable email detected. Please use a different mailing id.',
            'redirect': None,
        })

    if cur_user.send_verification_code():
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
    EMAIL = request.GET.get('email')
    PASSWORD = request.GET.get('password')
    VERIFICATION_CODE = request.GET.get('code')

    # In case an verification_code is provided
    if VERIFICATION_CODE != None:
        try:
            # Checking user status in existing database
            cur_user = Users.objects.get(EMAIL)
            cur_user_status = cur_user.user_status()
            if cur_user_status == 0:
                return JsonResponse({
                    'success': 0,
                    'message': 'Sorry, the user has been blocked or deleted.',
                    'redirect': None,
                })
            elif cur_user_status == 1 or cur_user_status == 2:
                if cur_user.match_verification_code(VERIFICATION_CODE) or cur_user_status == 2:
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
    if EMAIL == None or EMAIL.strip() == "" or PASSWORD == None or PASSWORD.strip() == "":
        return JsonResponse({
            'success': 0,
            'message': 'Please provide both email & password.',
            'redirect': None,
        })

    # Checking if both email & password aren't very long in length
    if len(EMAIL.strip()) > 100 or len(PASSWORD.strip()) > 20:
        return JsonResponse({
            'success': 0,
            'message': 'Too long email or password.',
            'redirect': None,
        })

    PASSWORD = helpers.generate_hash(PASSWORD)

    try:
        # Checking user status in existing database
        cur_user = Users.objects.get(email=EMAIL)
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
            if cur_user.password == PASSWORD:
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


def image_resizer(request, user_token):
    FILE_URL = request.GET.get('file')
    WIDTH = request.GET.get('width')
    HEIGHT = request.GET.get('height')

    try:
        assert FILE_URL
        WIDTH = int(WIDTH)
        HEIGHT = int(HEIGHT)
    except:
        return JsonResponse({
            'success': 0,
            'message': 'Invalid inputs.',
            'redirect': None,
        })

    try:
        cur_user = Users.objects.get(api_token=user_token)
        if (cur_user_status := cur_user.user_status()) != 2:
            if cur_user_status == 0:
                return JsonResponse({
                    'success': 0,
                    'message': 'Sorry, the user has been blocked or deleted.',
                    'redirect': None,
                })
            elif cur_user_status == 1:
                return JsonResponse({
                    'success': 0,
                    'message': 'User hasn\'t been verified.',
                    'redirect': '\verify',
                })
        if (usage_permission := cur_user.is_api_usage_allowed()) != 1:
            if usage_permission == 0:
                return JsonResponse({
                    'success': 0,
                    'message': 'Sorry, usage limit already reached on current plan.',
                    'redirect': None,
                })
            elif usage_permission == 2:
                return JsonResponse({
                    'success': 0,
                    'message': 'Unknown Exception Occurred! Please contact Harsh Raj (harshraj2717@gmail.com).',
                    'redirect': None,
                })
        try:
            output_url, file_transfer_size = helpers.resize_image(
                FILE_URL, WIDTH, HEIGHT)
            cur_user.use_resources(file_transfer_size)
            return JsonResponse({
                'success': 1,
                'message': output_url,
                'redirect': None,
            })
        except Exception as e:
            return JsonResponse({
                'success': 0,
                'message': e,
                'redirect': None,
            })
    except Users.DoesNotExist:
        return JsonResponse({
            'success': 0,
            'message': 'Invalid Token.',
            'redirect': '/login',
        })


def video_to_mp3(request, user_token):
    FILE_URL = request.GET.get('file')

    if not FILE_URL:
        return JsonResponse({
            'success': 0,
            'message': 'Invalid inputs.',
            'redirect': None,
        })

    try:
        cur_user = Users.objects.get(api_token=user_token)
        if (cur_user_status := cur_user.user_status()) != 2:
            if cur_user_status == 0:
                return JsonResponse({
                    'success': 0,
                    'message': 'Sorry, the user has been blocked or deleted.',
                    'redirect': None,
                })
            elif cur_user_status == 1:
                return JsonResponse({
                    'success': 0,
                    'message': 'User hasn\'t been verified.',
                    'redirect': '\verify',
                })
        if (usage_permission := cur_user.is_api_usage_allowed()) != 1:
            if usage_permission == 0:
                return JsonResponse({
                    'success': 0,
                    'message': 'Sorry, usage limit already reached on current plan.',
                    'redirect': None,
                })
            elif usage_permission == 2:
                return JsonResponse({
                    'success': 0,
                    'message': 'Unknown Exception Occurred! Please contact Harsh Raj (harshraj2717@gmail.com).',
                    'redirect': None,
                })
        try:
            output_url, file_transfer_size = helpers.video_to_mp3(FILE_URL)
            cur_user.use_resources(file_transfer_size)
            return JsonResponse({
                'success': 1,
                'message': output_url,
                'redirect': None,
            })
        except Exception as e:
            return JsonResponse({
                'success': 0,
                'message': e,
                'redirect': None,
            })
    except Users.DoesNotExist:
        return JsonResponse({
            'success': 0,
            'message': 'Invalid Token.',
            'redirect': '/login',
        })
