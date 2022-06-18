from django.db import models
from django.utils import timezone
import uuid


class CutDownUrl(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    origin_url = models.URLField()
    cutdown_url = models.URLField(db_index=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(CutDownUrl, self).save(*args, **kwargs)
