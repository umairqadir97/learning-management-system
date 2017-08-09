from django.conf.urls import url
from .views import QuizViewSet
from rest_framework.urlpatterns import format_suffix_patterns

quiz_list = QuizViewSet.as_view({
     'get': 'list',
     'post': 'create'   
})
 
 
quiz_detail = QuizViewSet.as_view({
     'get': 'retrieve',
     'put': 'update',
     'delete': 'destroy'
})
 
publish_quiz = QuizViewSet.as_view({
     'put': 'publish'
})
 
urlpatterns = format_suffix_patterns([
     url(r'^quizzes/$', quiz_list, name='quiz-list'),
     url(r'^quizzes/(?P<pk>[0-9])/$', quiz_detail, name='quiz-detail'),
     url(r'^quizzes/(?P<pk>[0-9])/publish/$', publish_quiz, name='publish-quiz'),
])
