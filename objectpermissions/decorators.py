try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.db.models import Model, get_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
try:
    from django.utils.decorators import auto_adapt_to_methods
except ImportError:
    auto_adapt_to_methods = lambda x: x
from django.utils.http import urlquote

from views import permission_denied

def permission_required(permission, obj_lookup, login_url=settings.LOGIN_URL, 
                        redirect_field_name=REDIRECT_FIELD_NAME, **kwargs):
    """
    Decorator for a view that makes sure that the user has *all* permissions,
    redirects to the log-in page if not logged in.
    
    :param permission: The permission set that the user must have for the object
    :type permission: An ``int``, ``string``, or ``list``
    :param obj_lookup: How to locate the object to test. It specifies the model,
                       `field and lookup <http://docs.djangoproject.com/en/dev/ref/models/querysets/#id7>`_,
                       and the name of the parameter containg the value to lookup
                       to retrieve the object
    :type obj_lookup: ``(<model>, '<field_lookup>', 'view_arg')`` or
                      ``('<appname>.<modelname>', '<field_lookup>', 'view_arg')``
    """
    if isinstance(obj_lookup, (tuple, list)):
        _model, lookup, varname = obj_lookup
    else:
        raise ValueError("The given argument '%s' should be a list or tuple" % obj_lookup)
    
    if issubclass(_model, Model):
        model = _model
    elif isinstance(_model, basestring):
        model = get_model(*model.split("."))
    else:
        raise ValueError("The model passed ('%s') is not a Model class or string in the format 'app.model'." % model)
    value = kwargs.get(varname, None)
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated():
                path = urlquote(request.get_full_path())
                return HttpResponseRedirect('%s?%s=%s' % (login_url, redirect_field_name, path))
            
            obj = get_object_or_404(model, **{lookup: value})
            if request.user.has_object_permission(obj, permission):
                return view_func(request, *args, **kwargs)
            return permission_denied(request)
        return wraps(view_func)(_wrapped_view)
    return auto_adapt_to_methods(decorator)
    