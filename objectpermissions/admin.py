from django import forms
from django.contrib.contenttypes import generic

from models import Permission, UserPermission, GroupPermission

class PermissionModelForm(forms.ModelForm):
    """
    A model form that represents the permissions as a multiple choice field.
    """
    perm_list = forms.MultipleChoiceField()
    
    class Meta:
        model=Permission
        exclude=['permission',]
    
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=forms.util.ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
        """
        We have to set the value for ``perm_list`` since it isn't a real field.
        
        The value from the instance is set as initial data.
        """
        if initial is None:
            initial = {}
        if instance is not None:
            initial['perm_list'] = instance.perm_list
        super(PermissionModelForm, self).__init__(data, files, auto_id, prefix,
                initial, error_class,label_suffix,empty_permitted, instance)
    
    def clean_perm_list(self):
        """
        Convert the list of number strings into a single integer value
        """
        self.cleaned_data['permission'] = reduce(lambda x,y: int(x)|int(y),self.cleaned_data['perm_list'])
    
    def save(self, commit=True):
        """
        Because ``permission`` was left out, it won't get saved. ``perm_list``
        won't get saved, since it isn't a real field. We set it here and let the
        parent class do the rest.
        """
        self.instance.permission = self.cleaned_data['permission']
        super(PermissionModelForm, self).save(commit)


class UserPermModelForm(PermissionModelForm):
    """
    Subclass the :class:`PermissionModelForm` for :class:`UserPermission`
    """
    class Meta:
        model=UserPermission

class GroupPermModelForm(PermissionModelForm):
    """
    Subclass the :class:`PermissionModelForm` for :class:`GroupPermission`
    """
    class Meta:
        model=GroupPermission


def inline_permission_form_factory(model, Form):
    class InlinePermissionModelForm(Form):
        perm_list = forms.MultipleChoiceField(choices=model.perms.choice_list())
    
    return InlinePermissionModelForm


class InlinePermissionModelAdmin(generic.GenericInlineModelAdmin):
    form = PermissionModelForm
    
    def __init__(self, parent_model, admin_site):
        self.form = inline_permission_form_factory(parent_model, self.form)
        super(InlinePermissionModelAdmin, self).__init__(parent_model, admin_site)


class TabularUserPermInline(InlinePermissionModelAdmin):
    form = UserPermModelForm
    model = UserPermission
    template = 'admin/edit_inline/tabular.html'
    exclude=['permission',]

class StackedUserPermInline(InlinePermissionModelAdmin):
    form = UserPermModelForm
    model=UserPermission
    template = 'admin/edit_inline/stacked.html'

class TabularGroupPermInline(InlinePermissionModelAdmin):
    form = GroupPermModelForm
    model = GroupPermission
    template = 'admin/edit_inline/tabular.html'
    exclude = ['permission',]

class StackedGroupPermInline(InlinePermissionModelAdmin):
    form = GroupPermModelForm
    model = GroupPermission
    template = 'admin/edit_inline/stacked.html'
