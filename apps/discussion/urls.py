from django.conf.urls import url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('topics', views.TopicViewSet)
router.register('entries', views.EntryViewSet)
# router.register('replies', views.ReplyViewSet)


urlpatterns = [
    # url(r'^', views.TopicListView.as_view(), name='list_topic'),
    url(r'^', include(router.urls)),

]
