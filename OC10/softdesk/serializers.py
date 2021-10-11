from rest_framework import serializers
from .models import Projects, Contributors, Issues, Comments


class ProjectSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Projects
        fields = ('id', 'title', 'description', 'type', 'author_user')
        extra_kwargs = {'author_user': {'read_only': True}}


class ContributorsSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Contributors
        fields = ('id', 'user', 'project', 'permission', 'role')
        extra_kwargs = {'project': {'read_only': True}}


class IssueSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Issues
        fields = ('id', 'title', 'description', 'tag', 'priority', 'project', 'status', 'author_user_id',
                  'assignee_user_id', 'created_time')
        extra_kwargs = {'created_time': {'read_only': True},
                        'author_user_id': {'read_only': True},
                        'project': {'read_only': True}}


class CommentSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Comments
        fields = ('id', 'description', 'author_user_id', 'issue_id', 'created_time')
        extra_kwargs = {'created_time': {'read_only': True},
                        'issue_id': {'read_only': True},
                        'author_user_id': {'read_only': True}}
