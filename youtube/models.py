from django.db import models
from tagging.validators import isTagList
from tagging.models import Tag, TaggedItem

class Video(models.Model):
    feed        = models.URLField()
    video_id    = models.CharField(max_length=50)
    published   = models.DateTimeField()
    updated     = models.DateTimeField()
    title       = models.CharField(max_length=250)
    author      = models.ForeignKey('User')
    description = models.TextField()
    tag_list    = models.CharField(max_length=250)
    view_count  = models.PositiveIntegerField()
    url         = models.URLField()
    thumbnail_url = models.URLField()
    length      = models.PositiveIntegerField()

    def _get_tags(self):
        return Tag.objects.get_for_object(self)
    def _set_tags(self, tag_list):
        Tag.objects.update_tags(self, tag_list)
    tags = property(_get_tags, _set_tags)

    def save(self):
        super(Video, self).save()
        Tag.objects.update_tags(self, self.tag_list)

    def embed_url(self):
        return u'http://www.youtube.com/v/%s' % self.video_id

    def __unicode__(self):
        return u'%s' % self.title

    class Admin:
        list_display = ('title', 'author', 'video_id', 'view_count')

class Playlist(models.Model):
    feed        = models.URLField()
    updated     = models.DateTimeField()
    title       = models.CharField(max_length=200)
    description = models.TextField()
    author      = models.ForeignKey('User')
    url         = models.URLField()
    videos      = models.ManyToManyField('PlaylistVideo')

    def __unicode__(self):
        return u'%s' % self.title

    def numVideos(self):
        return self.videos.count()

    class Admin:
        list_display = ('title', 'description', 'author', 'numVideos')

class PlaylistVideo(models.Model):
    feed        = models.URLField()
    title       = models.CharField(max_length=250)
    description = models.TextField()
    original    = models.ForeignKey('Video')

    def __unicode__(self):
        return u'%s' % self.title

    class Admin:
        list_display = ('title', 'description')
    
class User(models.Model):
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'))
    feed        = models.URLField()
    username    = models.CharField(max_length=50)
    first_name  = models.CharField(max_length=50)
    age         = models.PositiveIntegerField(null=True, blank=True)
    gender      = models.CharField(max_length=1, choices=GENDER_CHOICES)
    thumbnail_url = models.URLField()
    watch_count = models.PositiveIntegerField()
    url         = models.URLField()
    playlists   = models.ManyToManyField('Playlist')
    favorites   = models.ManyToManyField('Video')

    def __unicode__(self):
        return u'%s' % self.username

    class Admin:
        list_display = ('username', 'first_name', 'age', 'gender', 'watch_count')
