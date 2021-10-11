from django.db import models, utils
from django.conf import settings
from .exceptions import UniqueContributors


class Projects(models.Model):
    TYPE_CHOICES = (
        ('back-end', 'back_end'),
        ('front-end', 'front_end'),
        ('iOS', 'IOS'),
        ('Android', 'Android')
    )
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)


class Contributors(models.Model):
    PERMISSIONS_CHOICES = (
        ('CR', 'CR'),
        ('CRUD', 'CRUD')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, blank=True, on_delete=models.CASCADE)
    permission = models.CharField(max_length=255, choices=PERMISSIONS_CHOICES)
    role = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'project'], name='unique_contributors_for_project')
        ]

    def save(self, *args, **kwargs):
        try:
            super(Contributors, self).save(*args, **kwargs)
        except utils.IntegrityError:
            raise UniqueContributors()


class Issues(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    tag = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    project = models.ForeignKey(Projects, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name='author_user_id')
    assignee_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
                                         related_name='assignee_user_id')
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    description = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
