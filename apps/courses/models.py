from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


# We can now start discussion on it, that what we need to add more here.
# It is just a prototype
class Courses(models.Model):
    title = models.CharField(max_length=200)
    number = models.CharField(max_length=10)
    description = models.TextField()
    owner = models.ForeignKey(User, related_name=_('course'), null=True, blank=True)
    members = models.ManyToManyField(User, related_name=_('Members'), null=True, blank=True)
    hidden = models.BooleanField(default=False, blank=True)
    enrollment_start_date = models.DateTimeField()
    enrollment_end_date = models.DateTimeField()
    start_date = models.DateTimeField()
    slug = models.SlugField(max_length=100, db_index=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
