from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# from quiz.views import QuizVewSet
# from assignments import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'quizzes', QuizViewSet)
# router.register(r'v1/courses/(?P<course_slug>[\w-]+)/assignments', views.AssignmentViewSet)
# router.register(r'v1/assignments/submissions', views.StudentAssignmentViewSet)
    
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),

    # Apps
    # url(r'^', include(router.urls, namespace='assignments')),
    url(r'^', include('accounts.urls')),
    # url(r'^course/', include('courses.urls')),
    # url(r'^discussion/', include('discussion.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
