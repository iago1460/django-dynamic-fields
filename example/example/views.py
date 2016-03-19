from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django_dynamic_fields.form_mixins import DynamicFormMixin
from example.forms import SurveyForm
from example.models import Survey


class HomeView(DynamicFormMixin, CreateView):
    template_name = 'home.html'
    form_class = SurveyForm
    model = Survey

    def form_valid(self, form):
        self.object = form.save()
        values = []
        for field in self.model._meta.get_fields():
            if field.name not in ('id', 'hstore_data'):
                if hasattr(field, 'verbose_name'):
                    verbose_name = unicode(getattr(field, 'verbose_name'))
                else:
                    verbose_name = field.name

                display_function = 'get_%s_display' % field.name
                if hasattr(self.object, display_function):
                    display_value = getattr(self.object, display_function)()
                else:
                    display_value = unicode(getattr(self.object, field.name))
                values.append((verbose_name, display_value))

        context = self.get_context_data()
        context.update({
            'values': values
        })
        return render(self.request, 'survey_sent.html', context)
