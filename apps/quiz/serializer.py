from rest_framework import serializers
from discussion.models import DiscussionTopic, DiscussionEntry


class TopicSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = DiscussionTopic
        exclude = ('slug',)


class ReplySerializer(serializers.ModelSerializer):
	class Meta:
		model = DiscussionEntry
		fields = '__all__'

class EntrySerializer(serializers.ModelSerializer):
   replies = ReplySerializer(many=True, read_only=True)

   class Meta:
		model = DiscussionEntry
		fields = ('body', 'user', 'created','attachment', 'replies', )

   def perform_create(self, serializer):
    	serializer.save(owner=self.request.user)