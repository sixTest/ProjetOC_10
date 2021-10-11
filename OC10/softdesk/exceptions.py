from rest_framework.exceptions import APIException
from rest_framework import status


class UniqueContributors(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'This contributor already exists for this project'
    default_code = 'unique_constraint_failed'
