import json

from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Meeting, MeetingInviteLink
from .serializers import MeetingSerializer
from .services import create_meeting, user_joined_the_meeting, get_users_for_meeting


class MeetingViewSet(viewsets.ModelViewSet):
    serializer_class = MeetingSerializer
    # queryset = Meeting.objects.all()\
    #     .prefetch_related(
    #     Prefetch('meetinginvitelink', queryset=MeetingInviteLink.objects.all()
    #              .only('join_url'))
    # )

    # permission_classes = (IsAdminUser, )

    # def get_queryset(self):
    #     print("Запрос", self.request)
    #     team_id = self.request.team_id
    #     return Meeting.objects.filter(team_id=team_id)

    def list(self, request: Request, team_id):
        print("TeamId", team_id)
        meetings = Meeting.objects.filter(team_id=team_id)
        return Response({'meetings': MeetingSerializer(meetings, many=True).data})

    def create(self, request: Request, *args, **kwargs):
        body = request.data
        print(body)
        meeting = create_meeting(body)
        print("MEETING FROM CREATE", meeting)
        print("MEETING ID FROM CREATE", meeting.id)
        return Response({'meeting': MeetingSerializer(meeting).data})
        # return HttpResponse(meeting, content_type='application/json')

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass


def join_user_for_meeting(request):
    body = json.loads(request.body)
    print(body)
    user_joined_the_meeting(data={'meeting_id': body['meeting_id'], 'joined_user_id': body['user_id'],
                                  'username': body['username'], 'user_email': body['user_email'],
                                  'user_img_src': body['user_img_src']})
    return HttpResponse(json.dumps(body), content_type='application/json')


def fetch_users_for_meeting(request):
    body = json.loads(request.body)
    print(body)
    users = get_users_for_meeting(body['meeting_id'])
    return HttpResponse(json.dumps(users), content_type='application/json')


def index(request):
    return render(request, 'index.html')


def create_meeting_handler(request):
    body = json.loads(request.body)
    print(body)
    meeting = create_meeting(body)
    resp = MeetingSerializer(meeting).data
    return HttpResponse(resp, content_type='application/json')


def test(request):
    print("IN TEST HANDLER")
    return HttpResponse('test')
