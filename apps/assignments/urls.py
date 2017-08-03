from django.conf.urls import url
from .views import (
    AssignmentViewSet, 
    StudentAssignmentViewSet
)
from rest_framework.urlpatterns import format_suffix_patterns


assignment_list = AssignmentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})


assignment_detail = AssignmentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy' #This should be a logic delete?
})

publish_assignment = AssignmentViewSet.as_view({
    'put': 'publish'
})

assignment_submission = StudentAssignmentViewSet.as_view({
    'get': 'retrieve',
    'post': 'submit_response',
    'post': 'comment_submission'
})


urlpatterns = format_suffix_patterns([
    url(r'^assignments/$', assignment_list, name='assignment-list'),
    url(r'^assignments/(?P<pk>[0-9]+)/$', assignment_detail, name='assignment-detail'),
    url(r'^assignments/(?P<pk>[0-9]+)/publish/$', publish_assignment, name='publish-assignment'),
    url(r'^submissions/(?P<pk>[0-9]+)$', assignment_submission, name='submission'),
])