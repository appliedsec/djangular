from django.views.generic.base import TemplateView


class DjangularModuleTemplateView(TemplateView):
    content_type = 'text/javascript'
    template_name = 'djangular_module.js'
    disable_csrf_headers = False

    def get_context_data(self, **kwargs):
        context = super(DjangularModuleTemplateView, self).get_context_data(**kwargs)
        context['disable_csrf_headers'] = self.disable_csrf_headers
        return context
