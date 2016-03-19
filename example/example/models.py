from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django_dynamic_fields.models import HstoreModel


@python_2_unicode_compatible
class Survey(HstoreModel):
    name = models.CharField(max_length=255, verbose_name='What is your name?')

    def __str__(self):
        return '%s' % self.name
