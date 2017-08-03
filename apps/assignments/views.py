from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser

from .custom_viewsets import (
		CreateListRetrieveUpdateViewSet,
		RetrieveUpdateViewSet
	)

from .models import (
		Assignment, 
		AssignmentSubmission, 
		StudentAssignmentDate
	)

from .serializers import (
		AssignmentSerializer, 
		AssignmentDetailListSerializer, 
		AssigmentSubmissionDetailSerializer, 
		AssignmentSubmissionSerializer,
		AssignmentSubmissionCommentsSerializer,
		AssignmentSubmissionComments
	)



class AssignmentViewSet(CreateListRetrieveUpdateViewSet):
	"""
	API endpoint that allows a user to create or update assignments.
	---
	"""
	queryset = Assignment.objects.all()
	serializer_class = AssignmentSerializer
 	permission_classes = (permissions.AllowAny,)

	def get_serializer_class(self):
		#Depending of the request user, we should switch serializers here. 
		# if self.action == 'list':
		# 	return AssignmentDetailListSerializer
		return super(AssignmentViewSet, self).get_serializer_class()

	def get_queryset(self):
		#Should we filter by slug or course id???
		#We should check here if the request.user is part of the course otherwise throw an exception
		qs = self.queryset.filter(
				course__slug=self.kwargs.get('course_slug'),
				deleted=False
			)
		
		#Students should only see published assignments, intructors published, and non publish
		# if request.user.is_student:
		# 	qs = queryset.filter(published=True)

		return qs


	#Should we create different methods if we want user to 
	#publish/delete multiples assignments at the same time?
	@detail_route(methods=['put'])
	def publish(self, request, *args, **kwargs):
		assignment = self.get_object()
		assignment.published = not assignment.published
		assignment.save()
		return Response(assignment.published)

	@detail_route(methods=['put'])
	def delete(self, request, *args, **kwargs):
		assignment = self.get_object()
		assignment.deleted = True
		assignment.save()
		return Response(assignment.deleted)


class StudentAssignmentViewSet(RetrieveUpdateViewSet):
	queryset = StudentAssignmentDate.objects.all()
	serializer_class = AssigmentSubmissionDetailSerializer
	permission_classes = (permissions.AllowAny,)
	parser_classes = (MultiPartParser,JSONParser,)

	@detail_route(methods=['post'])
	def submit_response(self, request, *args, **kwargs):
		
		student_assignment = self.get_object()
		#If the user re-submit the assignment, previous submissions should be deleted? 
		for submission in student_assignment.submissions.all():
			submission.delete()
		
		serializer = AssignmentSubmissionSerializer(data=request.data)
		
		if serializer.is_valid():
			serializer.save(student_assignment_date=student_assignment)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			

	@detail_route(methods=['post'])
	def comment_submission(self, request, *args, **kwargs):
		
		student_assignment = self.get_object()
		serializer = AssignmentSubmissionCommentsSerializer(data=request.data)
		
		if serializer.is_valid():
			serializer.save(user=request.user, student_assignment_date=student_assignment)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


