from datetime import date
from django.db import models

# Create your models here.

USAGE_LIMITS = {
    0: (50, 25),
    1: (200, 100),
    2: (-1, -1),
}


class Users(models.Model):
    email = models.EmailField(
        unique=True,
        primary_key=True,
    )
    password = models.CharField(max_length=65)
    api_token = models.CharField(max_length=65)
    verified = models.BooleanField(default=False)
    cur_otp = models.CharField(max_length=65)
    active = models.BooleanField(default=False)
    # tier-0 == Free, 1 == Pro, 2 == Unlimited
    tier = models.PositiveSmallIntegerField(default=0)
    files_transferred_mb = models.PositiveIntegerField(default=0)
    api_calls_count = models.PositiveIntegerField(default=0)
    last_api_call_month = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.email

    def is_api_usage_allowed(self) -> int:
        '''
        tells if the object is allowed to use the API
            returns 0 == False, 1 == True, 2 == Error
        '''
        if self.tier > 2:
            # Somehow - Invalid Tier
            return 2
        elif self.last_api_call_month.month == date.today().month - 1:
            # A new month started
            self.files_transferred_mb = 0
            self.api_calls_count = 0
        elif self.tier != 2:
            # Not an unlimited tier user
            if (self.files_transferred_mb >= USAGE_LIMITS[self.tier][0]
                    or self.api_calls_count >= USAGE_LIMITS[self.tier][1]):
                return 0
        return 1

    def send_otp(self) -> bool:
        '''
        TODO
        Generate a random 6-digit OTP

        Send the OTP to provided email_id

        Return the success status (True/False) after sending mail
        '''
        ...

    def match_otp(self, otp: str) -> bool:
        '''
        TODO
        Match the provided otp with email_id's cur_otp

        Set verified = True and cur_otp = "" for the provided email_id

        Send a mail confirming account verification to the provided email_id

        Return the match status (True/False) after sending mail
        '''
        ...

    def is_email_disposable(self) -> bool:
        '''
        TODO
        Check if provided email_id is a disposable using https://www.mailcheck.ai/
        '''
        ...

    def user_status(self) -> int:
        '''
        TODO
        Check and return user status as:
            0 == Not-active (Deleted/Blocked),
            1 == Not-verified
            2 == Active
        '''
        ...
