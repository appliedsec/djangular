from django import template
from django.shortcuts import render_to_response

def angular_module(request):
    """
    Create the djangular angular app, which includes the django app dependencies needed.
    """
    return render_to_response('app.js', context_instance=template.RequestContext(request), mimetype='text/javascript')