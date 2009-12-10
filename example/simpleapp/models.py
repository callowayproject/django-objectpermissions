from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class SimpleText(models.Model):
    """A Testing app"""
    firstname = models.CharField(blank=True, max_length=255)
    lastname = models.CharField(blank=True, max_length=255)
    favorite_color = models.CharField(blank=True, max_length=255)
    
    def __unicode__(self):
        return self.firstname

class SimpleTaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.tag

import objectpermissions
permissions = ['perm1', 'perm2', 'perm3', 'perm4']
objectpermissions.register(SimpleText, permissions)

from django.contrib import admin
from objectpermissions.admin import TabularUserPermInline, StackedUserPermInline

class SimpleTextAdmin(admin.ModelAdmin):
    list_display = ('firstname','lastname','favorite_color')
    inlines = [TabularUserPermInline, ]

admin.site.register(SimpleText, SimpleTextAdmin)