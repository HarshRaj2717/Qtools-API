from . import models

def send_otp(email_id: str) -> int:
    '''
    Generate a random 6-digit OTP
    Send the OTP to provided email_id
    Return the same OTP
    '''
    ...


def is_email_disposable(email_id: str) -> bool:
    '''
    Check if provided email_id is a disposable using https://www.mailcheck.ai/
    '''
    ...


def user_status(email_id: str) -> int:
    '''
    Check and return user status as:
        0 == Not available,
        1 == Active,
        2 == Not-active (Deleted)
    '''
    ...
