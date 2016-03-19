from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.forms import modelform_factory
from django_dynamic_fields.models import DynamicField


class DynamicFormMixin(object):
    model = None
    fields = None
    form_class = None

    def get_form_class(self):
        model = self.model or self.form_class._meta.model
        if not model:
            raise ImproperlyConfigured(
                "DynamicFormMixin needs a model or a form_class with model defined"
            )
        if self.fields:
            fields = self.fields
        elif self.form_class and self.form_class.Meta.fields:
            fields = self.form_class.Meta.fields
        else:
            raise ImproperlyConfigured(
                "DynamicFormMixin needs fields or a form_class with fields defined"
            )
        if fields == '__all__':
            fields = [field.name for field in model._meta.get_fields() if field.name not in ('id', 'hstore_data')]
        else:
            extra_fields = DynamicField.objects.filter(content_types=ContentType.objects.get_for_model(model)).distinct()
            extra_fields = [extra_field.field_name for extra_field in extra_fields if extra_field.field_name not in fields]
            fields = fields + extra_fields
        if self.form_class:
            return modelform_factory(model, form=self.form_class, fields=fields)
        else:
            return modelform_factory(model, fields=fields)
