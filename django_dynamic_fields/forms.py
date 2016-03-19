from django import forms
from django.contrib.contenttypes.models import ContentType
from django_dynamic_fields.models import HstoreModel


class ExtraFieldAdminForm(forms.ModelForm):

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExtraFieldAdminForm, self).__init__(*args, **kwargs)
        content_type_ids = [
            content_type.id for content_type in ContentType.objects.all() if issubclass(content_type.model_class(), HstoreModel)
        ]
        self.fields['content_types'].queryset = ContentType.objects.filter(id__in=content_type_ids)
