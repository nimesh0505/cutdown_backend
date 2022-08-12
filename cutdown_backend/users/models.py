import random
import string

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def get_prefix_uuid(prefix_code: str) -> str:
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    return f"{prefix_code}{random_string}"


class CustomUser(User):
    user_id = models.CharField(max_length=30, unique=True, editable=False)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
            self.user_id = get_prefix_uuid("usr_")
        self.modified_at = timezone.now()
        return super(CustomUser, self).save(*args, **kwargs)
