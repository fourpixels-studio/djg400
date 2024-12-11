from django.db import models
from django.utils import timezone
from django.utils.dateformat import DateFormat


class Newsletter(models.Model):
    email = models.EmailField()
    subscribed_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    consent = models.BooleanField(default=True)
    resubscribed_at = models.DateTimeField(blank=True, null=True)

    @property
    def get_subscription_date(self):
        if self.resubscribed_at:
            date_format = DateFormat(self.resubscribed_at.astimezone(timezone.get_current_timezone()))
            formatted_date = date_format.format('M. d, Y')
        else:
            date_format = DateFormat(self.subscribed_at.astimezone(timezone.get_current_timezone()))
            formatted_date = date_format.format('M. d, Y')
        return formatted_date

    @property
    def get_unsubscription_date(self):
        try:
            date_format = DateFormat(self.unsubscribed_at.astimezone(timezone.get_current_timezone()))
            formatted_date = date_format.format('M. d, Y')
        except:
            formatted_date = "N/A"
        return formatted_date

    def __str__(self):
        if self.consent == True:
            subscription_status = f"Subscribed on {self.get_subscription_date}"
        else:
            if self.unsubscribed_at:
                subscription_status = f"Unsubscribed on {self.get_unsubscription_date}"
            else:
                subscription_status = "Not Subscribed"

        return f"{self.email} | {subscription_status}"
