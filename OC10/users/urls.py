from django.urls import path
from .views import RegisterView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('signup/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
