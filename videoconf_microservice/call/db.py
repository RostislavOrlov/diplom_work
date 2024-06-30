from .models import Meeting, MeetingsUsers, MeetingRole, MeetingSettings
from django.db import transaction


def plan_meeting_db():
    pass


def create_meeting_db(meeting_details):
    with transaction.atomic():
        meeting_settings = MeetingSettings(
            # is_planned=meeting_details.is_planned,
            # entry_before_the_organizer_is_enabled=meeting_details.entry_before_the_organizer_is_enabled,
            off_participants_voice_after_entry=meeting_details['off_participants_voice_after_entry'],
            is_on_waiting_hall=meeting_details['waiting_hall'],
        )
        meeting_settings.save()
        meeting = Meeting(
            theme=meeting_details['theme'],
            team_id=meeting_details['team_id'],
            user_registrant_id=meeting_details['user_registrant_id'],
            user_registrant_username=meeting_details['user_registrant_username'],
            user_registrant_email=meeting_details['user_registrant_email'],
            is_launched=meeting_details['is_launched'],
            start_date=meeting_details['start_date'],
            settings=meeting_settings,
            is_on_waiting_hall=meeting_details['waiting_hall'],
        )
        meeting.save()

        MeetingsUsers.objects.create(
            meeting_id=meeting.id,
            user_id=meeting_details['user_registrant_id'],
            username=meeting_details['user_registrant_username'],
            user_email=meeting_details['user_registrant_email'],
            user_duration=0,
            user_role=MeetingRole.OWNER,
        )

        print("MEETING DETAILS", meeting_details)
        print("MEETING", meeting.id)
        # transaction.commit()
    return meeting


def start_meeting_db(pk):
    meeting = Meeting.objects.get(pk=pk)
    meeting.is_launched = True
    meeting.save()


def edit_meeting_settings_db(meeting_settings, pk):
    meeting = Meeting.objects.get(pk=pk)
    meeting.settings = meeting_settings
    meeting.save()


def finish_meeting_db(pk):
    meeting = Meeting.objects.get(pk=pk)
    meeting.is_launched = False
    meeting.save()


def get_meetings_for_team_db(team_id):
    meetings = Meeting.objects.filter(team_id=team_id).order_by()


def get_session_rooms_for_meeting_db():
    pass


def create_session_room_for_meeting_db():
    pass


# def edit_session_room_for_meeting_db():
#     pass


def delete_session_room_for_meeting_db():
    pass


def start_recording_meeting_db():
    pass


def finish_recording_meeting_db():
    pass


# def change_microphone_state_db():
#     pass
#
#
# def change_camera_state_db():
#     pass


def get_users_for_meeting_db(pk):
    users = list(MeetingsUsers.objects.filter(meeting_id=pk).values_list('user_id'))
    users = [user[0] for user in users]
    return users


def get_users_details_for_meeting_db(pk):
    users = list(MeetingsUsers.objects.filter(meeting_id=pk).values('user_id', 'username', 'user_email', 'user_img_ref', 'user_role'))
    return users


def get_users_for_meeting_session_rooms_db():
    pass
