from discussion.models import DiscussionTopic, DiscussionEntry
from discussion.serializers import EntrySerializer, TopicSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import detail_route



class TopicViewSet(viewsets.ModelViewSet):
    """
    will be used to create new discussion and list existing discussions

    """
    queryset = DiscussionTopic.objects.all()
    serializer_class = TopicSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    @detail_route(methods=['post'],
                  authentication_classes=[BasicAuthentication],
                  permission_classes=[IsAuthenticated])
    def subscribe(self, request, *args, **kwargs):
        topic = self.get_object()
        topic.subscribers.add(request.user)
        return Response({'subscribe': True})


 
class EntryViewSet(viewsets.ModelViewSet):
    """
    will be used to add entries to a topic
    """
    queryset = DiscussionEntry.objects.filter(hidden = False)
    serializer_class = EntrySerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)


class ReplyViewSet(viewsets.ModelViewSet):
    serializer_class = EntrySerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)