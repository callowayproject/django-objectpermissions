from django.test import TestCase
from django.test.client import Client
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
# Test against flat pages

import objectpermissions
from models import ModelPermissions, UserPermission, GroupPermission
from simpleapp.models import SimpleText, SimpleTaggedItem

class TestModelPermissions(TestCase):
    perms = ['Perm1', 'Perm2', 'Perm3', 'Perm4']
    values = [1,2,4,8]

    def testObjectCapabilities(self):
        mp = ModelPermissions(self.perms)
        
        self.assertEquals(mp.Perm1, 1)
        self.assertEquals(mp.Perm2, 2)
        self.assertEquals(mp.Perm3, 4)
        self.assertEquals(mp.Perm4, 8)
    
    def testDictCapabilities(self):
        mp = ModelPermissions(self.perms)
        
        self.assertEquals(mp['Perm1'], 1)
        self.assertEquals(mp['Perm2'], 2)
        self.assertEquals(mp['Perm3'], 4)
        self.assertEquals(mp['Perm4'], 8)
        
        self.assertTrue('Perm3' in mp)
        self.assertFalse('Perm5' in mp)
        
        self.assertEquals(mp.keys(), self.perms)
        self.assertEquals(mp.values(), self.values)
    
    def testConversion(self):
        mp = ModelPermissions(self.perms)
        
        self.assertEquals(mp.as_int('Perm1'), 1)
        self.assertEquals(mp.as_int(['Perm1', 'Perm2', 'Perm4']), 1 | 2 | 8)
        self.assertEquals(mp.as_int(['Perm3', 'Perm2', 'Perm4']), 4 | 2 | 8)
        self.assertRaises(AttributeError, mp.as_int, ['Perm5', 'Perm2', 'Perm4'])

class TestRegistration(TestCase):
    perms = ['Perm1', 'Perm2', 'Perm3', 'Perm4']
    values = [1,2,4,8]
    fixtures = ['simpleapp.json', ]
    
    def setUp(self):
        self.fp = FlatPage.objects.create(url='dummy/', title="dummy", enable_comments=False, registration_required=False)
        try:
            objectpermissions.register(FlatPage, self.perms)
        except objectpermissions.AlreadyRegistered:
            pass
        self.fp.save()
        
        self.u = User.objects.create_user('simple_guy','simple@guy.com', 'password')
        self.g = Group(name="simple_group")
        self.g.save()
    
    def create_simpletext(self):
        self.st = SimpleText.objects.create(lastname="Daniels",
                                            favorite_color="Red",
                                            firstname="Charlie")
        self.st.simpletaggeditem_set.create(tag="country")
        self.st.simpletaggeditem_set.create(tag="singer")
        
    def testRegiser(self):
        self.assertTrue(hasattr(FlatPage, 'user_perms_set'))
        self.assertTrue(hasattr(FlatPage, 'group_perms_set'))
        self.assertTrue(hasattr(FlatPage, 'perms'))
    
    def testGrantUserPermissions(self):
        fp = self.fp
        u = self.u
        
        u.grant_object_perm(fp, fp.perms.Perm1)
        self.assertTrue(u.has_object_perm(fp, fp.perms.Perm1))
        self.assertFalse(u.has_object_perm(fp, fp.perms.Perm2))
        self.assertFalse(u.has_object_perm(fp, fp.perms.Perm3))
        self.assertTrue(u.has_object_perm(fp, [fp.perms.Perm1+fp.perms.Perm2]))
        self.assertTrue(u.has_any_object_perm(fp, [fp.perms.Perm1+fp.perms.Perm2]))
        self.assertFalse(u.has_all_object_perm(fp, [fp.perms.Perm1+fp.perms.Perm2]))
        
        
        up = UserPermission.objects.get(user=self.u)
        self.assertEquals(up.permission, fp.perms.Perm1)
        self.assertEquals(up.content_type, ContentType.objects.get_for_model(FlatPage))
        self.assertEquals(up.object_id, fp.id)
        
        self.assertEquals(fp.perms.as_string_list(13), ['Perm1', 'Perm3', 'Perm4'])
        self.assertEquals(fp.perms.as_int_list(13), [1,4,8])
        self.assertEquals(fp.perms.as_choices(13), [(1,'Perm1'),(4,'Perm3'),(8,'Perm4')])
        
        u.grant_object_perm(fp, [fp.perms.Perm2, fp.perms.Perm3])
        up = UserPermission.objects.get(user=self.u)
        self.assertEquals(up.content_type, ContentType.objects.get_for_model(FlatPage))
        self.assertEquals(up.object_id, fp.id)
        self.assertEquals(up.permission, fp.perms.Perm1 | fp.perms.Perm2 | fp.perms.Perm3)
    
    def testRevokeUserPermission(self):
        fp = self.fp
        u = self.u
        
        u.grant_object_perm(fp, fp.perms.Perm1)
        self.assertTrue(u.has_object_perm(fp, fp.perms.Perm1))
        
        u.revoke_object_perm(fp, fp.perms.Perm1)
        self.assertFalse(u.has_object_perm(fp, fp.perms.Perm1))
    
    
    def testGetUserPermissions(self):
        fp = self.fp
        u = self.u
        g = self.g
        g.user_set.add(u)
        
        # Clean the slate
        u.revoke_all_object_perm(fp)
        g.revoke_all_object_perm(fp)
        self.assertEquals(u.get_object_perm(fp), 0)
        self.assertEquals(g.get_object_perm(fp), 0)
        self.assertEquals(u.get_object_perm_as_str_list(fp), [])
        self.assertEquals(g.get_object_perm_as_str_list(fp), [])
        
        u.grant_object_perm(fp, fp.perms.Perm1 + fp.perms.Perm4)
        self.assertEquals(u.get_object_perm(fp), 9)
        self.assertEquals(u.get_object_perm_as_str_list(fp), ['Perm1', 'Perm4'])
        self.assertEquals(u.get_object_perm_as_int_list(fp), [1, 8])
        self.assertEquals(u.get_object_perm_as_choices(fp), [(1, 'Perm1'), (8,'Perm4')])
        
        # Test that the group permissions work correctly with the user perms
        g.grant_object_perm(fp, fp.perms.Perm1+fp.perms.Perm3)
        self.assertEquals(u.get_object_perm(fp), fp.perms.Perm1+fp.perms.Perm3+fp.perms.Perm4)
        
        # Revoking the Perm1 for the user, shouldn't change anything because
        # The group also has it
        u.revoke_object_perm(fp, fp.perms.Perm1)
        self.assertEquals(u.get_object_perm(fp), fp.perms.Perm1+fp.perms.Perm3+fp.perms.Perm4)
        
        g.revoke_object_perm(fp, fp.perms.Perm1)
        self.assertEquals(u.get_object_perm(fp), fp.perms.Perm3+fp.perms.Perm4)
    
    def testGetObjectsWithPermission(self):
        fp = self.fp
        u = self.u
        g = self.g
        
        # Clean the slate
        u.revoke_all_object_perm(fp)
        g.revoke_all_object_perm(fp)
        self.assertEquals(u.get_object_perm(fp), 0)
        self.assertEquals(g.get_object_perm(fp), 0)
        
        g.grant_object_perm(fp, fp.perms.Perm1 + fp.perms.Perm4)
        objs = u.get_objects_with_perms(FlatPage, fp.perms.Perm4)
        self.assertEquals(len(objs), 0)
        
        g.user_set.add(u)
        objs = u.get_objects_with_perms(FlatPage, fp.perms.Perm1)
        self.assertEquals(fp, objs[0])
        objs = u.get_objects_with_perms(FlatPage, fp.perms.Perm2)
        self.assertEquals(len(objs), 0)
        
    
    def testSignals(self):
        self.create_simpletext()
        st = self.st
        u = self.u
        g = self.g
        g.user_set.add(u)
        
        def my_user_handler(sender, to_whom, to_what, **kwargs):
            self.assertTrue(isinstance(sender, UserPermission))
            if isinstance(to_what, SimpleText):
                stis = to_what.simpletaggeditem_set.all()
                for item in stis:
                    to_whom.set_object_perm(item, sender.permission)
            else:
                self.assertTrue(isinstance(to_what, SimpleTaggedItem))
        
        def my_group_handler(sender, to_whom, to_what, **kwargs):
            self.assertTrue(isinstance(sender, GroupPermission))
            if isinstance(to_what, SimpleText):
                stis = to_what.simpletaggeditem_set.all()
                for item in stis:
                    to_whom.set_object_perm(item, sender.permission)
            else:
                self.assertTrue(isinstance(to_what, SimpleTaggedItem))
        
        from signals import permission_changed
        permission_changed.connect(my_user_handler)
        
        u.grant_object_perm(st, st.perms.perm1)
        for item in st.simpletaggeditem_set.all():
            self.assertEquals(u.get_object_perm(item), u.get_object_perm(st))
        permission_changed.disconnect(my_user_handler)
        permission_changed.connect(my_group_handler)
        g.grant_object_perm(st, st.perms.perm2)
        for item in st.simpletaggeditem_set.all():
            self.assertEquals(u.get_object_perm(item), u.get_object_perm(st))
        
        
