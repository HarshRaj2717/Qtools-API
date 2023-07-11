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
    verified = models.BooleanField()
    active = models.BooleanField()
    tier = models.PositiveSmallIntegerField()  # 0 == Free, 1 == Pro, 2 == Unlimited
    files_transferred_mb = models.PositiveIntegerField()
    api_calls_count = models.PositiveIntegerField()
    last_api_call_month = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.email

    def is_usage_allowed(self) -> int:
        # 0 == False, 1 == True, 2 == Error
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
