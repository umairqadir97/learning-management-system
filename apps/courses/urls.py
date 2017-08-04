from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^details/(?P<slug>[^/]+)/$', CourseDetails.as_view(), name='course-details'),
    url(r'^update/(?P<slug>[^/]+)/$', CourseDetails.as_view(), name='course-update'),
    url(r'^remove/(?P<slug>[^/]+)/$', CourseDetails.as_view(), name='course-remove'),
    url(r'^list/$', CourseList.as_view(), name='course-list'),

]
