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
    simple_text = models.ForeignKey(SimpleText)

    def __unicode__(self):
        return self.tag

import objectpermissions
permissions = ['perm1', 'perm2', 'perm3', 'perm4']
objectpermissions.register(SimpleText, permissions)
objectpermissions.register(SimpleTaggedItem, permissions)

from django.contrib import admin
from objectpermissions.admin import TabularUserPermInline, StackedUserPermInline

class SimpleTaggedItemInline(admin.TabularInline):
    model = SimpleTaggedItem

class SimpleTextAdmin(admin.ModelAdmin):
    list_display = ('firstname','lastname','favorite_color')
    inlines = [SimpleTaggedItemInline, TabularUserPermInline, ]

admin.site.register(SimpleText, SimpleTextAdmin)