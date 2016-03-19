from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django_dynamic_fields.models import DynamicField, DynamicFieldChoice
from django_dynamic_fields.utils import update_schemas
from example.models import Survey


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Create administrator user
        user, created = User.objects.get_or_create(
            username='admin', defaults={
                'is_superuser': True,
                'is_staff': True,
            }
        )
        if created:
            user.set_password('1234')
            user.save()

        # Create Survey fields
        survey_content_type = ContentType.objects.get_for_model(Survey)
        dynamic_field, created = DynamicField.objects.get_or_create(
            verbose_name='How old are you?',
            field_name='age',
            type='IntegerField',
        )
        dynamic_field.content_types.add(survey_content_type)

        dynamic_field, created = DynamicField.objects.get_or_create(
            verbose_name='Do you have any brother or sisters?',
            field_name='siblings',
            type='BooleanField',
        )
        dynamic_field.content_types.add(survey_content_type)

        dynamic_field, created = DynamicField.objects.get_or_create(
            verbose_name='What color are you eyes?',
            field_name='eyes',
            type='IntegerField',
        )
        dynamic_field.content_types.add(survey_content_type)
        colors = ('Black', 'Brown', 'Hazel', 'Grey', 'Green', 'Blue',)
        for color in colors:
            DynamicFieldChoice.objects.get_or_create(dynamic_field=dynamic_field, name=color)

        dynamic_field, created = DynamicField.objects.get_or_create(
            verbose_name='What is your e-mail address?',
            field_name='email',
            type='EmailField',
            blank=True,
            help_text='The email is not mandatory',
        )
        dynamic_field.content_types.add(survey_content_type)
