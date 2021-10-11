from rest_framework.permissions import IsAuthenticated
from .permissions import ProjectsPermissions, ContributorsPermissions, IssuesPermissions, CommentsPermissions
from .serializers import ProjectSerializer, ContributorsSerializer, IssueSerializer, CommentSerializer
from .models import Projects, Contributors, Issues, Comments
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin

User = get_user_model()


class ProjectsViewsSet(ModelViewSet):
    """
        Urls :
        -projects/
        -projects/<pk>/

        Permissions:
            - method POST : all authenticated users can create a project
            - method GET (list) : all authenticated users can use this method but will only have access to projects where
                                  they are contributors
            - method GET (retrieve) : all authenticated users can use this method to access project details only if
                                      they are contributors
            - method DELETE/PUT : All authenticated users with CRUD permission on the project can access these methods
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectsPermissions]

    def perform_create(self, serializer):
        project = serializer.save(author_user=self.request.user)
        Contributors(user=self.request.user, project=project, permission='CRUD', role='AUTHOR').save()

    def get_queryset(self):
        projects_id = [cont.project.id for cont in Contributors.objects.filter(user=self.request.user)]
        return Projects.objects.filter(id__in=projects_id)


class ContributorsViewsSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    """
        Urls :
        - projects/<nested_1_pk>/users/
        - projects/<nested_1_pk>/users/<pk>/

        Permissions:
            - method POST : All authenticated users with CRUD permission on the project can create a project contributor
            - method GET (list) : All authenticated users being project contributors can access the list of users
                                  composing the project
            - method DELETE :
                - 1/ All authenticated users with CRUD permission can delete a project contributor
                - 2/ An authenticated contributor may delete itself

        Warnings :
            -Adding the PUT method without changing permissions may result in safety issues
    """
    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated, ContributorsPermissions]

    def perform_create(self, serializer):
        serializer.save(project=Projects.objects.filter(id=self.kwargs['nested_1_pk']).first())

    def get_queryset(self):
        if self.action == 'list':
            users_id = [cont.user.id for cont in Contributors.objects.filter(project=int(self.kwargs['nested_1_pk']))]
            return User.objects.filter(id__in=users_id)
        else:
            return Contributors.objects.filter(project=int(self.kwargs['nested_1_pk']))

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        else:
            return self.serializer_class


class IssuesViewsSet(ModelViewSet):
    """
        Urls:
        - projects/<nested_1_pk>/issues/
        - projects/<nested_1_pk>/issues/<pk>/

        Permissions:
            - method POST : All authenticated users who are contributors to the project can create an issue
            - method GET (list/retrieve) : All authenticated users who are contributors to the project can have access
                                           to these methods
            - method DELETE/PUT :
                - 1/ All authenticated users with CRUD permission on the project can access these methods
                - 2/ An authenticated user who is the author of the issue may have access to these methods
    """
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IssuesPermissions]

    def get_queryset(self):
        return Issues.objects.filter(project=int(self.kwargs['nested_1_pk']))

    def perform_create(self, serializer):
        serializer.save(author_user_id=self.request.user,
                        project=Projects.objects.get(id=int(self.kwargs['nested_1_pk'])))


class CommentsViewsSet(ModelViewSet):
    """
        Urls:
        - projects/<nested_1_pk>/issues/<nested_2_pk>/comments/
        - projects/<nested_1_pk>/issues/<nested_2_pk>/comments/<pk>/

        Permissions:
            - method POST : all authenticated users who are contributors to the project can create a comment relating to
                            any problem belonging to the project
            - method GET (list/retrieve) : All authenticated users who are contributors to the project can have access
                                           to these methods
            - method DELETE/PUT :
                - 1/ All authenticated users with CRUD permission on the project can access these methods
                - 2/ An authenticated user who is the author of the comment may have access to these methods
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CommentsPermissions]

    def get_queryset(self):
        return Comments.objects.filter(issue_id=self.kwargs['nested_2_pk'])

    def perform_create(self, serializer):
        serializer.save(author_user_id=self.request.user, issue_id=Issues.objects.get(id=int(self.kwargs['nested_2_pk'])))


