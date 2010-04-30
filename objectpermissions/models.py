from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class UnknownPermission(Exception):
    """
    An attempt was made to query for a permission that was not registered for that model.
    """
    pass


class PermissionManager(models.Manager):
    def all_with_perm(self, permission):
        """
        Return all users that have the permission ``permission`` for this object.
        """
        perm = self.instance.perms.as_int(permission)
        qs = self.get_query_set()
        new_qs = qs.extra(where=['permission & %s = %s',], params=[perm, perm])
        return new_qs


class Permission(models.Model):
    """
    A privilege granted to a specific User or Group to a specific object.
    """
    permission = models.IntegerField(null=True, blank=True, default=0)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        abstract = True
    
    objects = PermissionManager()
    
    @classmethod
    def bits(self, a):
        """
        Convert an integer into a list of 1's or 0's indicating the
        bits set. Modified from http://wiki.python.org/moin/BitManipulation
        
        >>> Permission.bits(10)
        [0, 0, 1, 0, 1, 0]
        
        :param a: The integer to convert
        :type a: ``integer``
        :result: A list of ``1`` and ``0`` corresponding to a bit set or not
        """
        result = []
        oct_bits={'0':[0,0,0],'1':[0,0,1],'2':[0,1,0],'3':[0,1,1],
           '4':[1,0,0],'5':[1,0,1],'6':[1,1,0],'7':[1,1,1]}
        for c in filter(lambda char: char != 'L', oct(a))[1:]:
                result += oct_bits[c]
        return result
    
    @classmethod
    def int_to_perms(self, a):
        """
        Convert an integer used to represent a bitwise setting of integers into a 
        list of integers corresponding to the values of the bits set in the integer.
        
        >>> Permission.int_to_perms(10)
        [8, 2]
        
        :param a: The bitwise permission to convert
        :type a: ``integer``
        :result: A list of integers corresponding to values of the set bits
        """
        result=[]
        bitlist = self.bits(a)
        l = len(bitlist)
        for i in range(l):
            result.insert(0, 1<<i)
        return [i for i in map(lambda x,y: x*y, bitlist, result) if i != 0]
    
    
    def _set_perm_with_list(self, int_list):
        """
        Set the permissions from an integer list
        """
        if isinstance(int_list, int):
            self.permission = int_list
            return
        elif not isinstance(int_list, (list, tuple)):
            raise Exception("The parameter %s is not a list or tuple" % int_list)
        self.permission = reduce(lambda x,y: x | y, int_list)
    
    def _get_perm_as_list(self):
        """
        Return the permission as a list of integers
        """
        return self.int_to_perms(self.permission)
    
    perm_list = property(_get_perm_as_list, _set_perm_with_list, doc="The permissions as an integer list")

class UserPermission(Permission):
    user = models.ForeignKey(User)
    
    def save(self, *a, **kw):
        """
        Send out a signal indicating that a permission was changed
        """
        super(Permission, self).save(*a, **kw)
        from signals import permission_changed
        permission_changed.send(sender=self, to_whom=self.user, to_what=self.content_object)


class GroupPermission(Permission):
    group = models.ForeignKey(Group, null=True)
    
    def save(self, *a, **kw):
        """
        Send out a signal indicating that a permission was changed
        """
        super(Permission, self).save(*a, **kw)
        from signals import permission_changed
        permission_changed.send(sender=self, to_whom=self.group, to_what=self.content_object)


class ModelPermissions(object):
    """
    An object that converts named permissions into a bitwise set of attributes
    """
    def __init__(self, permissions):
        self._perms = permissions[:]
        for num, perm in enumerate(permissions):
            setattr(self, perm, 1<<num)
    
    def __len__(self):
        return len(self._perms)
    
    def __getitem__(self, key):
        if key in self._perms:
            return getattr(self, key)
        else:
            raise KeyError
    
    def __iter__(self):
        for item in self._perms:
            yield item
    
    def iterkeys(self):
        return self.__iter__()
    
    def itervalues(self):
        for item in self._perms:
            yield getattr(self, item)
    
    def keys(self):
        return self._perms
    
    def values(self):
        return [getattr(self, x) for x in self._perms]
    
    def has_key(self, key):
        return self.__contains__(key)
    
    def __contains__(self, value):
        return value in self._perms
    
    def items(self):
        return [(getattr(self, key), key) for key in self._perms]
    
    def as_int(self, perm):
        """
        A utility method to convert several types of arguments into the integer representation.
        
        Converts strings by looking up the name
        Converts a list or tuple by OR'ing the int value for each item
        """
        if isinstance(perm, int):
            valid_perm = perm
        elif isinstance(perm, basestring):
            # Look up the attribute, it will raise an error if it doesn't exist
            valid_perm = getattr(self, perm)
        elif isinstance(perm, (list, tuple)):
            valid_perm = 0
            for item in perm:
                valid_perm |= self.as_int(item)
        else:
            raise UnknownPermission("'%s' is an unknown permission type." % perm)
        return valid_perm
    
    def as_string_list(self, perm):
        """
        A utility method to convert an integer into a list of strings of the selected permissions
        """
        if not isinstance(perm, int):
            raise UnknownPermission("'perm' must be an integer")
        result_list = []
        for key, val in self.items():
            if key & perm == key:
                result_list.append(val)
        return result_list
    
    def as_int_list(self, perm):
        """
        A utility method to convert an integer into a list of integers of the selected permissions
        """
        if not isinstance(perm, int):
            raise UnknownPermission("'perm' must be an integer")
        result_list = []
        for key, val in self.items():
            if key & perm == key:
                result_list.append(key)
        return result_list
        
    def as_choices(self, perm):
        """
        A utility method to convert an integer into a list of integer, string tuples for choices
        """
        if not isinstance(perm, int):
            raise UnknownPermission("'perm' must be an integer")
        result_list = []
        for key, val in self.items():
            if key & perm == key:
                result_list.append((key, val))
        return result_list
    
    def choice_list(self):
        """
        Return a list of integer,string tuples for a choice list
        """
        return self.items()


class UserPermissionRelation(generic.GenericRelation):
    """A generic relation for Object Permissions"""
    
    def __init__(self,**kwargs):
        """Override this to automatically set the "to" field """
        super(UserPermissionRelation, self).__init__(UserPermission, **kwargs)


class GroupPermissionRelation(generic.GenericRelation):
    """A generic relation for Object Permissions"""
    
    def __init__(self,**kwargs):
        """Override this to automatically set the "to" field """
        super(GroupPermissionRelation, self).__init__(GroupPermission, **kwargs)

