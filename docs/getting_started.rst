===============
Getting Started
===============


Install it

Add it to INSTALLED_APPS

Tutorial for setting up a model/admin/view:
	Existing or 3rd-party app
	Ground up

permissions in python

reference

Registering Permissions for a Model
===================================

To enable object permissions for a model, you must first register the model somewhere. ``models.py`` is a good place if you have control of the code, but it can be in ``settings.py`` or any other place that Django automatically imports.

Registering a model consists of calling the :func:`objectpermissions.register` function with a list or tuple of permission names. ::

	class SimpleText(models.Model):
	    firstname = models.CharField(blank=True, max_length=255)
	    lastname = models.CharField(blank=True, max_length=255)
	    favorite_color = models.CharField(blank=True, max_length=255)

	    def __unicode__(self):
	        return self.firstname
	
	import objectpermissions
	permissions = ['perm1', 'perm2', 'perm3', 'perm4']
	objectpermissions.register(SimpleText, permissions)

However, the model that you register doesn't have to be your own. For example, to add object permissions to the :class:`FlatPage` model::

	from django.contrib.flatpages.models import FlatPage
	import objectpermissions
	perms = ['read', 'write', 'own', 'delete']
	objectpermissions.register(FlatPage, perms)


Admin Setup
===========

There are four ``InlineModelAdmin`` classes to add to your ``ModelAdmin.inlines`` list: a tabular and stacked version for user permissions and group permissions.

* ``TabularUserPermInline``
* ``StackedUserPermInline``
* ``TabularGroupPermInline``
* ``StackedGroupPermInline``

::

	from objectpermissions.admin import TabularUserPermInline, TabularGroupPermInline

	class SimpleTextAdmin(admin.ModelAdmin):
	    list_display = ('firstname','lastname','favorite_color')
	    inlines = [TabularUserPermInline, TabularGroupPermInline]

	admin.site.register(SimpleText, SimpleTextAdmin)

If you are modifying an existing model and you do not want to modify its source, for example the FlatPage contrib app, you can unregister its admin, modify it and re-register it. ::

	from django.contrib import admin
	from django.contrib.flatpages.models import FlatPage
	from django.contrib.flatpages.admin import FlatPageAdmin
	from objectpermissions.admin import TabularUserPermInline, TabularGroupPermInline

	class MyFlatPageAdmin(FlatPageAdmin):
	    inlines = [TabularUserPermInline, TabularGroupPermInline]

	admin.site.unregister(FlatPage)
	admin.site.register(FlatPage, MyFlatPageAdmin)


Specifying Permission Sets
==========================

Permissions can be passed as an int, using the object's (or model's) ``perms`` attribute::

    obj.perms.perm1 + obj.perms.perm2

Permissions can be referenced by name::

    'perm1'

Permissions can be referenced by a list of names or ``int``\ s::

    ['perm1', 'perm2']
    [obj.perms.perm1, objs.perms.perm2]


Granting Permissions
====================

Granting permissions to a user or group for an object requires calling the ``grant_object_perm`` method on the user or group::

	>>> from django.contrib.auth.models import User, Group
	>>> from django.contrib.flatpages.models import FlatPage

	# Get the User, Group and FlatPage objects
	>>> user = User.objects.get(username="jimbob")
	>>> group = Group.objects.get(name="admins")
	>>> flatpg = FlatPage.objects.get(url="/private/stuff/")

	# Grant the permissions
	>>> user.grant_object_perm(flatpg, flatpg.perms.read + flatpg.perms.write)
	>>> group.grant_object_perm(flatpg, flatpg.perms.delete)

You can also grant permissions by string or list of strings::

	>>> user.grant_object_perm(flatpg, ['read','write'])
	>>> group.grant_object_perm(flatpg, 'delete')


Testing for Permissions
=======================

Django Object Permissions is only a framework for storing and managing permissions. Since the permissions can mean anything to any model, at some point you will have to write code to see if the user attempting to do something has the appropriate permission.

There basic method for checking permissions is ``has_object_perm``\ . There are two explicit variations: ``has_any_object_perm`` and ``has_all_object_perm``\ . The third parameter of ``has_object_perm`` allows you to optionally make sure that the user or group has all of the permissions pass to the function.

For example, continuing the above example::

	>>> user.has_object_perm(flatpg, flatpg.perms.delete)
	False
	
	# By default it checks that the user has any of the permissions
	# and the user has write permission
	>>> user.has_object_perm(flatpg, flatpg.perms.delete + flatpg.perms.write)
	True
	
	# Explicit version of the default has_object_perm functionality
	>>> user.has_any_object_perm(flatpg, flatpg.perms.delete + flatpg.perms.write)
	True
	
	# Explicit check that the user has both delete and write permissions
	>>> user.has_all_object_perm(flatpg, flatpg.perms.delete + flatpg.perms.write)
	False

When testing a user's permissions, it checks all the group's in which the user belongs. For example, continuing from above::

	>>> user.groups.add(group)
	
	# The user has read and write permisison, the group has delete permission
	# by adding the user to the group, it inherits delete permission
	>>> user.has_object_perm(flatpg, flatpg.perms.delete)
	True


