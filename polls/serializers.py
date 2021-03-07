"""
Polls application serializers.
"""

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_201_CREATED
from django.contrib.auth import get_user_model

from .models import Poll, Choice, Vote


class UserSerializer(serializers.ModelSerializer):
    """
    User model serializer.
    """

    username = serializers.CharField(
        required=True, min_length=6, max_length=150)
    email = serializers.EmailField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = self.Meta.model(
            email=validated_data['email'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        Token.objects.create(user=user)

        return Response(status=HTTP_201_CREATED)


class VoteSerializer(serializers.ModelSerializer):
    """
    Vote model serializer.
    """

    class Meta:
        model = Vote
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    """
    Poll model serializer.
    """

    question = serializers.CharField(min_length=10, max_length=144)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'date', 'question', 'user')

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id

        return super().create(validated_data)


class ChoiceSerializer(serializers.ModelSerializer):
    """
    Choice model serializer.
    """

    poll = PollSerializer(read_only=True)
    poll_id = serializers.IntegerField(required=True, min_value=1)
    votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Choice
        fields = ('poll', 'poll_id', 'text', 'votes')
