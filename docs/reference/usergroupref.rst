.. _usergroupref:

========================
User and Group Reference
========================

These methods are added to each :class:`User` and :class:`Group` instance.

* :func:`grant_object_perm`
* :func:`revoke_object_perm`
* :func:`set_object_perm`
* :func:`revoke_all_object_perm`
* :func:`has_object_perm`
* :func:`has_any_object_perm`
* :func:`has_all_object_perm`
* :func:`get_object_perm`
* :func:`get_object_perm_as_str_list`
* :func:`get_object_perm_as_int_list`
* :func:`get_object_perm_as_choices`
* :func:`get_objects_with_perms`

.. function:: grant_object_perm(self, instance, perm)
   
   Grants permission ``perm`` to object ``instance`` for the :class:`User` or 
   :class:`Group` ``self``\ .
   
   This function is added to the :class:`User` and :class:`Group` models and 
   is called as::
   
       a_user.grant_object_perm(an_object_instance, 'read')
   
   :param instance: A Django :class:`Model` instance
   :type instance: :class:`Model`
   :param perm: The permission(s) to grant
   :type perm: ``integer``, ``string``, ``list of string``


.. function:: revoke_object_perm(self, instance, perm)
   
   Remove the permission ``perm`` to object ``instance`` for the :class:`User` or :class:`Group` ``self``\ .

   :param instance: A Django :class:`Model` instance
   :type instance: :class:`Model`
   :param perm: The name of the permission to revoke
   :type perm: ``integer``, ``string``, ``list of string``


.. function:: revoke_all_object_perm(self, instance)
   
   Remove all the permissions for this :class:`User` or :class:`Group`\ .
   
   :param instance: A Django :class:`Model` instance
   :type instance: :class:`Model`


.. function:: set_object_perm(self, instance, perm)
   
   Sets the permission to the ``perm`` value. Same as revoking all privileges
   and granting ``perm``
   
   :param instance: The object on which to set the permissions
   :type instance:  ``Model``
   :param perm:  The permission(s) that should be set.
   :type perm:   ``int``, ``string`` or ``list of string``


.. function:: has_object_perm(self, instance, perm, require_all=False)
   
   Basic testing of user permissions. Does :class:`User` or :class:`Group` have permission ``perm`` for object ``instance``\ . When passing in multiple permissions, you can force the checking that the :class:`User` or :class:`Group` has *all* the permissions by passing ``True`` as the third parameter. By default it returns ``True`` if the :class:`User` or :class:`Group` has *any* of the permissions.
   
   For :class:`User`\ s, it will return ``True`` if any of the :class:`Group`\ s in which they are a member has ``perm``\ .
   
   Superusers *always* return ``True``
   
   Inactive users *always* return ``False``
   
   :param instance: The object for which the user may or may not have permissions.
   :type instance:  A Django model subclass that has been registered with :func:`objectpermissions.register`
   :param perm:     Permission(s) to check for in either an integer, a string or a list of strings
   :type perm:      ``int``, ``string`` or ``list of string``
   :param require_all: Does the user need to have all the permissions? ``True``
                       if they do. **Default:** ``False``
   :type require_all:  ``bool``


.. function:: has_all_object_perm(self, instance, perm)
   
   A more descriptive short cut for :func:`has_object_perm` with ``require_all`` set to ``True``

.. function:: has_any_object_perm(self, instance, perm)
   
   A more descriptive short cut for :func:`has_object_perm` with ``require_all`` set to ``False``


.. function:: get_object_perm(self, instance, format='int')
   
   Get the :class:`User`\ 's or :class:`Group`\ 's permissions for this object, formatted in a specific way.
   
   :class:`User` objects return all permissions they have based on :class:`Group` membership.
   
   Format options:
   
   * int: One integer with all permissions
   
   * string_list: A list of the permission names
   
   * int_list: A list of the permission values
   
   * choices: A list of integer, string tuples for choice lists
   
   :param instance: A django :class:`Model` instance
   :type instance: :class:`Model`
   :param format: 'int', 'string_list', 'int_list', 'choices'. **Default:** 'int'
   :type format: ``string``


.. function:: get_object_perm_as_str_list(self, instance)

   A more descriptive short cut for :func:`get_object_perm` with ``format`` set to ``str_list``


.. function:: get_object_perm_as_int_list(self, instance)

   A more descriptive short cut for :func:`get_object_perm` with ``format`` set to ``int_list``

.. function:: get_object_perm_as_choices(self, instance)

   A more descriptive short cut for :func:`get_object_perm` with ``format`` set to ``choices``

.. function:: get_objects_with_perms(self, model, permission)
   
   Return all objects of type model where the :class:`User` or :class:`Group` has permission ``permission``\ .
   
   :class:`User` instances will include objects in which their :class:`Group`\ 's have permission as well.
   
   :param instance: A django :class:`Model` instance
   :type instance: :class:`Model`
   :param permission: 'int', 'string_list', 'int_list', 'choices'. **Default:** 'int'
   :type permission: ``string``

