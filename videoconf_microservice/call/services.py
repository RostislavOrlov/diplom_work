from datetime import datetime

from .db import create_meeting_db, edit_meeting_settings_db, get_users_for_meeting_db, get_users_details_for_meeting_db
from .models import MeetingsUsers, MeetingRole


def plan_meeting():
    pass


def create_meeting(meeting_details):
    meeting = create_meeting_db(meeting_details)
    return meeting


def edit_meeting_settings(meeting_settings, pk):
    meeting = edit_meeting_settings_db(meeting_settings, pk)


def finish_meeting():
    pass


def start_recording_meeting():
    pass


def finish_recording_meeting():
    pass


def user_joined_the_meeting(data):
    print("DATA MEETING ID", data['meeting_id'])
    users_ids = get_users_for_meeting_db(data['meeting_id'])
    if data['joined_user_id'] not in users_ids:
        instance = MeetingsUsers(
            meeting_id=data['meeting_id'],
            user_id=data['joined_user_id'],
            username=data['username'],
            ##user_img_ref=data['user_img_src'],
            user_email=data['user_email'],
            start_time=datetime.now(),
            is_attended_the_meeting=True,
            breaking_count=0,
            user_duration=0,
            user_role=MeetingRole.PARTICIPANT,
        )
        instance.save()


def get_users_for_meeting(meeting_id):
    users = get_users_details_for_meeting_db(meeting_id)
    return users
