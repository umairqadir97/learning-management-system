from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from assignments.models import Assignment, AssignmentGroup
## Further imports will be added here ##

# Students would be identified after submitting the quiz,
# as only students subscribed to a particular course can take its quizzes.
# However, this approach depends on the use of session ID, which could be risky.
# This is just a temporary solution though; the problem will be properly
# addressed once an alternative is figured out

class Quiz(models.Model):

    quiz_types = (
    ('PQ', 'Practice Quiz'),
     ('GQ', 'Graded Quiz'),
     ('GS', 'Graded Survey'),
     ('US', 'Ungraded Survey'))

    title = models.CharField(max_length=100)
    grade = models.PositiveIntegerField(default=0)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    assignment_group = models.ForeignKey(AssignmentGroup, on_delete=models.CASCADE)
    # context_module_tags = models.ForeignKey(ContentTag, on_delete=models.CASCADE) # Parent App Needed
    quiz_groups = models.ForeignKey('QuizGroup', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    quiz_questions = models.ManyToManyField('QuizQuestion', related_name='%(app_label)s_%(class)s_related')
    quiz_regrades = models.ForeignKey('QuizRegrade', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    quiz_statistics = models.ForeignKey('QuizStatistics', on_delete=models.CASCADE) # Parent App Needed
    quiz_submissions = models.ForeignKey('uizSubmission', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    instructions = models.TextField()
    deleted = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    allowed_attempts = models.PositiveIntegerField(default=1)
    one_question_at_a_time = models.BooleanField(default=False)
    quiz_type = models.CharField(max_length=2, choices=quiz_types, default='')
    due_date = models.DateTimeField(null=True, blank=True)
    available_from = models.DateTimeField(null=True, blank=True)
    available_to = models.DateTimeField(null=True, blank=True)
    notify_users_of_change = models.BooleanField(default=False)
    
    def __unicode__(self):

        return self.title


class QuizGroup(models.Model):

    assessment_question_bank = models.ForeignKey('AssessmentQuestionBank', on_delete=models.CASCADE) # Parent App Needed
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    quiz_questions = models.ForeignKey('QuizQuestion', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')


class QuizQuestion(models.Model):

    types = (
            ('MPC', 'Multiple Choice'),
            ('TOF', 'True/False'),
            ('FIB', 'Fill In the Blanks'),
            ('FMB', 'Fill In Multiple Blanks'),
            ('MAN', 'Multiple Answers'),
            ('MDD', 'Multiple Dropdowns'),
            ('MCH', 'Matching'),
            ('NMA', 'Numerical Answer'),
            ('FMQ', 'Formula Question'),
            ('ESQ', 'Essay Question'),
            ('FUQ', 'File Upload Question'),
            ('TXQ', 'Text Question (No Question)')
            )

    assessment_question = models.ForeignKey('AssessmentQuestion', on_delete=models.CASCADE) # Parent App Needed
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    quiz_group = models.ForeignKey(QuizGroup, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    point = models.IntegerField(default=0)
    question_type = models.CharField(max_length=3, choices=types, default='')


class QuizAnswer(models.Model):

    title = models.CharField(max_length=200)


class QuizQA(models.Model):

    question = models.ForeignKey('QuizQuestion', on_delete=models.CASCADE)
    answer = models.ForeignKey('QuizAnswer', on_delete=models.CASCADE)
    
            
class QuizRegrade(models.Model):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    quiz_question_regrades = models.ForeignKey('QuizQuestionRegrade', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    quiz_regrade_runs = models.ForeignKey('QuizRegradeRun', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class QuizSubmission(models.Model):

    events = models.ForeignKey('QuizSubmissionEvent', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class QuizQuestionRegrade(models.Model):

    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    quiz_regrade = models.ForeignKey(QuizRegrade, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')


class QuizRegradeRun(models.Model):

    quiz_regrade = models.ForeignKey(QuizRegrade, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')


class QuizSubmissionEvent(models.Model):

    quiz_submission = models.ForeignKey(QuizSubmission, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
