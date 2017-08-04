from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError


class DiscussionTopic(models.Model):
    """Model for a discussion topic"""
    title = models.CharField(max_length=60)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField(blank=True, default='')
    owner = models.ForeignKey(User, blank=True, null=True, related_name=_('owner'))
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    subscribers = models.ManyToManyField(User, related_name="topic_subscribers")
    attachment = models.FileField(upload_to='users/%Y/%m/%d', blank=True)
    is_followed = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    allow_liking = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    group_discussion = models.BooleanField(default=False)
    #group = models.ForeignKey(GroupCategory)

    class Meta:
        ordering = ["-created"]


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        #check for identical topic to avoid double posting
        topic_exists = DiscussionTopic.objects.filter(
            owner=self.owner, title=self.title)
        if topic_exists:
            raise ValidationError(_("This topic has already been created"))
        super(DiscussionTopic, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.title



class DiscussionEntry(models.Model):
    ''' Model for nested discussion entry'''
    MAX_REPLIES = 1
    body = models.TextField(blank=False)
    topic = models.ForeignKey(DiscussionTopic, related_name=_('Entries'))
    user = models.ForeignKey(User,  related_name=_('Entries'))
    parent = models.ForeignKey('self', verbose_name= _('Reply to'), null=True, blank=True, related_name=_('replies'))
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    attachment = models.FileField(upload_to='users/%Y/%m/%d', blank=True)
    edited = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Discussion Entries'
        ordering = ["-created"]

    def __unicode__(self):
        if self.parent == None:
            parent = self.topic
        else:
            parent = self.parent
        return 'Comment by {} on {}'.format(self.user, self.parent)