from django import template
from django.shortcuts import render_to_response
from django.conf import settings


def angular_module(request):
    """
    Create the djangular angular app, which includes the django app dependencies needed.
    """
    return render_to_response('app.js', context_instance=template.RequestContext(request, {
        'disable_csrf_headers': getattr(settings, 'DJANGULAR_DISABLE_CSRF_HEADERS', False)
    }), mimetype='text/javascript')
