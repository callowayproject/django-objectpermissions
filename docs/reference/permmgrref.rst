.. _permmgrref:

============================
Permission Manager Reference
============================

Each model that is registered to have object permissions has a :class:`PermissionManager` for :class:`UserPermission` and :class:`GroupPermission` relationships with an extra function:

* :func:`all_with_perm`

.. function:: all_with_perm(self, permission)
   
   Returns all :class:`ObjectPermission` objects that have the permission specified. It is very useful for getting all users or groups that have access to to this object.