from rest_framework import permissions
from .models import Contributors, Issues


class ProjectsPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True if Contributors.objects.filter(project=obj.id).filter(user=request.user.id) else False
        else:
            return True if Contributors.objects.filter(project=obj.id).filter(user=request.user.id, permission='CRUD') \
                else False


class ContributorsPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return True if Contributors.objects.filter(project=view.kwargs['nested_1_pk']).filter(user=request.user.id,
                                                                                                  permission='CRUD') \
                else False
        else:
            return True if Contributors.objects.filter(project=view.kwargs['nested_1_pk']).filter(user=request.user.id) \
                else False

    def has_object_permission(self, request, view, obj):
        return bool(Contributors.objects.filter(project=view.kwargs['nested_1_pk']).filter(user=request.user.id,
                                                                                           permission='CRUD')
                    or
                    request.user.id == obj.user.id)


class IssuesPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return True if Contributors.objects.filter(project=view.kwargs['nested_1_pk']).filter(user=request.user.id) \
            else False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        else:
            return bool(Contributors.objects.filter(project=view.kwargs['nested_1_pk']).filter(user=request.user.id,
                                                                                               permission='CRUD')
                        or
                        request.user.id == obj.author_user_id.id)


class CommentsPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            Contributors.objects.filter(project=view.kwargs['nested_1_pk']).filter(user=request.user.id)
            and
            Issues.objects.filter(id=view.kwargs['nested_2_pk'], project=view.kwargs['nested_1_pk'])
        )

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        else:
            return bool(Contributors.objects.filter(project=view.kwargs['nested_1_pk']).filter(user=request.user.id,
                                                                                               permission='CRUD')
                        or
                        request.user.id == obj.author_user_id.id)
