"""
Polls application API views.
"""

from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from .models import Choice, Poll, Vote
from .serializers import (
    ChoiceSerializer, PollSerializer, UserSerializer, VoteSerializer)


class ChoiceViewSet(ModelViewSet):
    """
    Model viewset for choices.
    """

    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        action = self.action

        if action != 'list':
            return super().get_queryset()

        queryset = self.queryset

        poll_id = self.request.query_params.get('poll_id', None)

        if poll_id:
            queryset = queryset.filter(poll_id=poll_id)

        return queryset

    def post(self, request, *args, **kwargs):
        """
        Create a new poll's choice.
        """
        poll = self.get_object()

        if request.user.id != poll.user.id:
            raise PermissionDenied("You can not create choice for this poll.")

        return super().post(request, *args, **kwargs)  # pylint: disable=no-member


class PollViewSet(ModelViewSet):
    """
    Model viewset for polls.
    """

    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Destroy a poll instance.
        """
        poll = self.get_object()

        if request.user.id != poll.user.id:
            raise PermissionDenied("You can not delete this poll.")

        return super().destroy(request, *args, **kwargs)  # pylint: disable=no-member


class UserCreate(GenericViewSet, CreateModelMixin):
    """
    Create users instances.
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class VoteViewSet(ModelViewSet):
    """
    Model viewset for votes.
    """

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

class LoginView(APIView):
    """
    Handles user login logic.
    """
    permission_classes = ()

    def post(self, request):
        """
        Checks user credentials.

        If user exists, will retrive authentication token.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            return Response({'token': user.auth_token.key})

        return Response(status=HTTP_401_UNAUTHORIZED)
