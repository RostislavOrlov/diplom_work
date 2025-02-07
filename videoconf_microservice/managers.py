from django.db import models


class MeetingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(is_launched=True)
