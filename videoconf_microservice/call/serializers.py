from rest_framework import serializers

from .models import Meeting, MeetingInviteLink, MeetingPoll, SessionRoom


class MeetingSerializer(serializers.ModelSerializer):

    # invite_link_url = serializers.CharField(source='meetinginvitelink.join_url')

    class Meta:
        model = Meeting
        fields = '__all__'


class MeetingLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingInviteLink
        fields = '__all__'


class MeetingPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingPoll
        fields = '__all__'


class SessionRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionRoom
        fields = '__all__'
