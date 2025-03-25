from django.db import models
from django.conf import settings
import datetime
from django.contrib.auth import get_user_model



class Articles(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    username = models.TextField(default="None")
    end_date = models.DateField(default=datetime.date.today)
    titles = models.TextField()
    text = models.TextField()
    level_importance = models.CharField(max_length=40)

    def __str__(self):
        return self.titles