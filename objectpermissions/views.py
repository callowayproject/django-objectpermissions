from django.http import HttpResponseForbidden #, HttpResponseRedirect, Http404
# from django.shortcuts import render_to_response
from django.template import loader, RequestContext
# from django.utils.translation import ugettext, ugettext_lazy as _


# modified from django-authority
def permission_denied(request, template_name=None, extra_context={}):
    """
    Default 403 handler.

    Templates: `403.html`
    Context:
        request_path
            The path of the requested URL (e.g., '/app/pages/bad_page/')
    """
    if template_name is None:
        template_name = ('403.html',)
    context = {
        'request_path': request.path,
    }
    context.update(extra_context)
    return HttpResponseForbidden(loader.render_to_string(template_name, context,
                                 context_instance=RequestContext(request)))
