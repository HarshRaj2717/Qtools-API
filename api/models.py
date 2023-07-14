import smtplib
from email.message import EmailMessage
from datetime import date
from random import randint
import requests
from django.db import models
from django.conf import settings
from . import helpers


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
    cur_code = models.CharField(max_length=65)
    active = models.BooleanField(default=True)
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
            self.save()
        elif self.tier != 2:
            # Not an unlimited tier user
            if (self.files_transferred_mb >= USAGE_LIMITS[self.tier][0]
                    or self.api_calls_count >= USAGE_LIMITS[self.tier][1]):
                return 0
        return 1

    def send_verification_code(self) -> bool:
        '''
        Generate a random 6-digit verification code

        Send the OTP to provided email_id

        Return the success status (True/False) after sending mail
        '''
        verification_code = str(randint(100000, 999999))
        self.cur_code = helpers.generate_hash(verification_code)

        msg = EmailMessage()
        msg['Subject'] = 'Verify your Qtools account!'
        msg['From'] = settings.EMAIL_ADDRESS
        msg['To'] = self.email
        msg.set_content(f'''
                        <!DOCTYPE html>
                        <html lang="en">
                        <body>
                            <p>
                            Please verify your for Qtools account. Here is your verification code:
                            </p>
                            <h3>{verification_code}</h3>
                            <p>
                            If you haven't attempted to register/login to
                            <a href="http://qtools.hraj.dev" target="_blank" rel="noopener noreferrer"
                                >Qtools</a
                            >
                            then please ignore this mail.
                            </p>
                            <hr>
                            <small>
                                <p>This is an automatically generated email; please don't reply. For any queries, contact (<a href="mailto:harshraj2717@gmail.com">harshraj2717@gmail.com</a>)</p>
                            </small>
                            <br>
                            <p>Regards:</p>
                            <p><em><a href="http://hraj.dev" target="_blank" rel="noopener noreferrer">Harsh Raj</a> (Developer & Maintainer, Qtools)</em></p>
                        </body>
                        </html>
                        ''', subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
            smtp.send_message(msg)

        return True

    def match_verification_code(self, verification_code: str) -> bool:
        '''
        Match the provided otp with email_id's cur_code

        Set verified = True and cur_otp = "" for the provided email_id

        Send a mail confirming account verification to the provided email_id

        Return the match status (True/False) after sending mail
        '''
        verification_code = helpers.generate_hash(verification_code)
        if verification_code == self.cur_code:
            self.cur_code = '.'
            self.verified = True
            self.save()

            msg = EmailMessage()
            msg['Subject'] = 'Welcome to Qtools!'
            msg['From'] = settings.EMAIL_ADDRESS
            msg['To'] = self.email
            msg.set_content(f'''
                            <!DOCTYPE html>
                            <html lang="en">
                            <body>
                                <h3>
                                🎉 Account verification successful!
                                </h3>
                                <p>
                                You are great 🙌. Enjoy the world of powerful tools designed to simplify your workflow and amplify your productivity now!
                                </p>
                                <hr>
                                <small>
                                    <p>This is an automatically generated email; please don't reply. For any queries, contact (<a href="mailto:harshraj2717@gmail.com">harshraj2717@gmail.com</a>)</p>
                                </small>
                                <br>
                                <p>Regards:</p>
                                <p><em><a href="http://hraj.dev" target="_blank" rel="noopener noreferrer">Harsh Raj</a> (Developer & Maintainer, Qtools)</em></p>
                            </body>
                            </html>
                            ''', subtype='html')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
                smtp.send_message(msg)

            return True
        else:
            return False

    def is_email_disposable(self) -> bool:
        '''
        Check if provided email_id is a disposable email using https://www.mailcheck.ai/
        '''
        mail_check_response = requests.get(
            f'https://api.mailcheck.ai/email/{self.email}')
        if mail_check_response.status_code != 200:
            msg = EmailMessage()
            msg['Subject'] = 'Qtools - Issues with mailcheck.ai!'
            msg['From'] = settings.EMAIL_ADDRESS
            msg['To'] = self.email
            msg.set_content(f'''
                            <!DOCTYPE html>
                            <html lang="en">
                            <body>
                                <p>
                                Issues detected with mailcheck.ai on Qtools website! All emails (disposable/non-disposable) will get disallowed from registration untill the issue is fixed.
                                </p>
                                <p>
                                mailcheck.ai reponse status code - {str(mail_check_response.status_code)}
                                </p>
                                <hr>
                                <small>
                                    <p>This is an automatically generated email; please don't reply. For any queries, contact (<a href="mailto:harshraj2717@gmail.com">harshraj2717@gmail.com</a>)</p>
                                </small>
                                <br>
                                <p>Regards:</p>
                                <p><em><a href="http://hraj.dev" target="_blank" rel="noopener noreferrer">Harsh Raj</a> (Developer & Maintainer, Qtools)</em></p>
                            </body>
                            </html>
                            ''', subtype='html')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
                smtp.send_message(msg)

            return True

        mail_check_response_json = mail_check_response.json()
        if mail_check_response_json['disposable'] == True:
            return True
        else:
            return False

    def user_status(self) -> int:
        '''
        Check and return user status as:
            0 == Not-active (Deleted/Blocked),
            1 == Active & Not-verified
            2 == Active & Verified
        '''
        if self.active == False:
            return 0
        if self.verified == False:
            return 1
        return 2
