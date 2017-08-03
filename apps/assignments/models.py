from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models



class TimeStampedModel(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	
	class Meta:
		abstract = True


class AssignmentGroup(models.Model):
	"""
	This model stores all groups created by Instructor
	"""
	name = models.CharField(max_length=200)
	percentage_of_total_grade = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name


class Course(models.Model):
	"""
	This model is for testing porpuses
	"""
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=100)

	def __unicode__(self):
		return self.name


class DisplayGrade(models.Model):
	"""
	Defines how the assignment grade is going to be displayed, options are:
	-Percentage 
	-Complete/Incomplete 
	-Points 
	-Letter Grade
	-GPA Scale 
	-Not Graded
	"""
	name = models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.name


class SubmissionType(models.Model):
	"""
	Defines how students can upload their assignment, options are:
	-No Submission 
	-Online 
	-On Paper 
	-External Tool
	"""
	name = models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.name


class Assignment(TimeStampedModel):
	"""
	This model define the assignment
	"""
	title = models.CharField(max_length=200)
	content = models.TextField()
	points = models.IntegerField(default=0)
	published = models.BooleanField(default=False)
	deleted = models.BooleanField(default=False)
	notify_users_content_changed = models.BooleanField(default=False)
	do_not_count_on_final_grade = models.BooleanField(default=False)
	moderate_grading = models.BooleanField(default=False)
	display_grade_as = models.ForeignKey(DisplayGrade, related_name='display_grade')
	course = models.ForeignKey(Course, related_name='course')
	group = models.ForeignKey(AssignmentGroup, related_name='group')	
	
	
	def __unicode__(self):
		return self.title


class AssignmentSubmissionOption(models.Model):
	"""
	Define options allowed, base on the submission type chosen for an assignment
	"""
	assignment = models.OneToOneField(Assignment, related_name='submission_options', primary_key=True)
	submission_type = models.ForeignKey(SubmissionType, related_name='submission_type')
	online_text_entry = models.BooleanField(default=False)
	online_url = models.BooleanField(default=False)
	media_recording = models.BooleanField(default=False)
	online_upload = models.BooleanField(default=False)
	allowed_extensions = models.TextField(blank=True)


class PeerReview(models.Model):
	"""
	Peer Review options for the assignment
	"""
	assignment = models.OneToOneField(Assignment, on_delete=models.CASCADE, primary_key=True, related_name='peer_review_options')
	required = models.BooleanField(default=False)
	manually_assign = models.BooleanField(default=False)
	automatically_assign = models.BooleanField(default=False)
	reviews_per_user = models.IntegerField(default=0)
	assign_reviews = models.DateField(blank=True, null=True)
	anonymity = models.BooleanField(default=False)


class AssignmentDate(models.Model):
	"""
	A model to stores all available dates for a given assignments
	"""
	assignment 	= models.ForeignKey(Assignment, related_name='assignments_dates')
	due_date = models.DateTimeField(null=True, blank=True)
	available_from = models.DateTimeField(null=True, blank=True)
	available_until = models.DateTimeField(null=True, blank=True)


class StudentAssignmentDate(models.Model):
	"""
	This model stores all relations between assignments and the student
	"""
	assignment_date = models.ForeignKey(AssignmentDate, related_name='students')
	student = models.ForeignKey(User)
	grade = models.IntegerField(default=0)


class AssignmentSubmissionComments(TimeStampedModel):
	"""
	This model stores comments made by the student and instructor according to 
	submissions
	"""
	user = models.ForeignKey(User)
	student_assignment_date = models.ForeignKey(StudentAssignmentDate, related_name='comments')
	attach_file = models.FileField(upload_to='uploads/', blank=True, null=True)
	comment = models.TextField(blank=True, null=True)

	class Meta:
		ordering = ["-created"]


class AssignmentSubmission(TimeStampedModel):
	"""
	This model stores all different submissions made by the student
	"""
	student_assignment_date = models.ForeignKey(StudentAssignmentDate, related_name='submissions')
	attach_file = models.FileField(upload_to='uploads/', blank=True, null=True)
	text_entry = models.TextField(blank=True, null=True)
	website_url = models.URLField(blank=True, null=True)

	class Meta:
		ordering = ["-created"]


class GroupCategory(models.Model):
	set_name = models.CharField(max_length=200)
	allow_self_sign_up = models.BooleanField(default=False)
	require_members_be_same_section = models.BooleanField(default=False)
	number_of_groups_to_create = models.IntegerField(default=1)
	create_groups_manually = models.BooleanField(default=False)
	max_members = models.IntegerField(default=2)
	automatically_assign_leader = models.BooleanField(default=False)
	set_first_student_leader = models.BooleanField(default=False)
	set_random_leader = models.BooleanField(default=False)
	course = models.ForeignKey(Course)