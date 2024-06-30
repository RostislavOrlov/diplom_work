from django.db import models


class PollType(models.TextChoices):
    POLL = "poll", "обычное голосование"
    QUIZ = "quiz", "квиз"
