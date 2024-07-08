from django.db import models

class Newsletter(models.Model):
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.email