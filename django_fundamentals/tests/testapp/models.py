from django.conf import settings
from django.db import models

from django_fundamentals.models import TimeStampedModel


class Note(TimeStampedModel):
    """*a minimal owned model, used only to exercise ownership/permission helpers in tests*"""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    class Meta:
        app_label = "fundamentals_testapp"
