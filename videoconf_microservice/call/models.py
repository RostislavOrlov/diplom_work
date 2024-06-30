from enum import Enum

from django.db import models

import managers
from .enums import PollType


class Profile(models.Model):
    """ User profile model """
    login = models.CharField(max_length=50, unique=True)
    channel_name = models.CharField(max_length=250, unique=True)


class MeetingSettings(models.Model):
    is_planned = models.BooleanField(default=True)
    entry_before_the_organizer_is_enabled = models.BooleanField(default=False)
    off_participants_voice_after_entry = models.BooleanField(default=True)
    is_on_waiting_hall = models.BooleanField(default=True)


class Meeting(models.Model):
    theme = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    duration = models.IntegerField(default=0)
    team_id = models.IntegerField()
    user_registrant_id = models.IntegerField()
    user_registrant_username = models.CharField(max_length=1000)
    user_registrant_email = models.CharField(max_length=1000)
    is_launched = models.BooleanField(default=False)
    # join_url = models.CharField(max_length=100)
    start_date = models.DateField()
    settings = models.OneToOneField(MeetingSettings, on_delete=models.CASCADE)
    is_on_waiting_hall = models.BooleanField(default=True)

    objects = models.Manager()
    active_launched = managers.MeetingManager()


class SessionRoom(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    max_participant_count = models.IntegerField()


class RoomsUsers(models.Model):
    room_id = models.IntegerField()
    user_id = models.IntegerField()
    user_duration = models.IntegerField()


class MeetingsUsers(models.Model):
    meeting_id = models.IntegerField()
    user_id = models.IntegerField()
    username = models.CharField(max_length=100)
    user_img_ref = models.CharField(max_length=10000)
    user_email = models.CharField(max_length=1000)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    is_attended_the_meeting = models.BooleanField(default=False)
    breaking_count = models.IntegerField(default=0)  # количество выходов пользователя из конференции
    user_duration = models.IntegerField(default=0)  # должно быть вычисляемым полем
    user_role = models.CharField(max_length=50)


class MeetingPoll(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.PROTECT)
    anonymous = models.BooleanField(default=False)
    poll_type = models.CharField(max_length=50, choices=PollType.choices, blank=False,
                                 default=PollType.POLL)
    question = models.CharField(max_length=1000)
    answer_options = models.CharField(max_length=1000)


class MeetingInviteLink(models.Model):
    meeting = models.OneToOneField(Meeting, on_delete=models.PROTECT)
    ttl = models.IntegerField()
    join_url = models.CharField(max_length=200)


class MeetingRole(Enum):
    OWNER = "Владелец"
    ADMIN = "Администратор"
    PARTICIPANT = "Участник"
