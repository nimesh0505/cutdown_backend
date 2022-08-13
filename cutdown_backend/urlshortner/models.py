import random
import string

from django.db import models
from django.utils import timezone
from users.models import CustomUser


def generate_random_string():
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))


class ShortenURL(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    origin_url = models.CharField(max_length=1000000)
    shorten_key = models.CharField(
        max_length=20, db_index=True, default=generate_random_string
    )
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(ShortenURL, self).save(*args, **kwargs)


class ShortenURLBasic(ShortenURL):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
