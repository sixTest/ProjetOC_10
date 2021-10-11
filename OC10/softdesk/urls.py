from .views import ProjectsViewsSet, ContributorsViewsSet, IssuesViewsSet, CommentsViewsSet
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter
from django.urls import path, include

router = DefaultRouter()
router.register('projects', ProjectsViewsSet, basename='projects')

contributors_router = NestedSimpleRouter(router, r'projects', 'projects')
contributors_router.register(r'users', ContributorsViewsSet, basename='contributors')

issues_router = NestedSimpleRouter(router, r'projects', 'projects')
issues_router.register(r'issues', IssuesViewsSet, basename='issues')

comments_router = NestedSimpleRouter(issues_router, r'issues', 'issues')
comments_router.register(r'comments', CommentsViewsSet, basename='comments')

urlpatterns = [path('', include(router.urls)),
               path('', include(contributors_router.urls)),
               path('', include(issues_router.urls)),
               path('', include(comments_router.urls))]

