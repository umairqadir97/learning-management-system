from rest_framework import viewsets
from .serializers import QuizSerializer
from .models import Quiz
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import detail_route


class QuizCreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):

    pass


class QuizViewSet(QuizCreateListRetrieveViewSet):
    
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):

        return super(QuizViewSet, self).get_serializer_class()

    def get_queryset(self):

        qs = self.queryset.filter(pk=self.kwargs.get('pk'), deleted=False)

        return qs

    def list(self, request):
        
        queryset = Quiz.objects.all()
        serializer = QuizSerializer(queryset, many=True)
        
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        
        queryset = Quiz.objects.all()
        quiz = get_object_or_404(queryset, pk=pk)
        serializer = QuizSerializer(quiz)
        
        return Response(serializer.data)

    @detail_route(methods=['put'])
    def publish(self, request, *args, **kwargs):
        
        quiz = self.get_object()
        quiz.published = not quiz.published
        quiz.save()
        return Response(quiz.published)

    @detail_route(methods=['put'])
    def archive(self, request, *args, **kwargs):

        quiz = self.get_object()

        if quiz.archived:
            
            quiz.archived = False
            quiz.published = False

        else:

            quiz.archived = True
            
        quiz.save()
        return Response(quiz.archived)

    @detail_route(methods=['put'])
    def delete(self, request, *args, **kwargs):
        
        quiz = self.get_object()
        quiz.deleted = True
        quiz.save()
        return Response(quiz.deleted)

    
