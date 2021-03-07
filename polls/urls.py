"""
Polls application URL configuration.
"""

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (
    ChoiceViewSet, LoginView, PollViewSet, UserCreate, VoteViewSet)


router = DefaultRouter()

router.register(r'choices', ChoiceViewSet, basename='choices')
router.register(r'polls', PollViewSet, basename='polls')
router.register(r'users', UserCreate, basename='users')
router.register(r'votes', VoteViewSet, basename='votes')


urlpatterns = [path(r'login/', LoginView.as_view(), name='login'),
               path(r'docs/', include_docs_urls(title='Polls API'))]

urlpatterns += router.urls
