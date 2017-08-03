from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class PasswordRecovery(models.Model):
    user = models.ForeignKey(User)
    creation_time = models.DateTimeField(default=datetime.now)
    secret_key = models.CharField(max_length=256)
    last_modified = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        db_table = 'password_recovery'
