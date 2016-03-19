from __future__ import unicode_literals
from django.contrib.postgres.operations import HStoreExtension

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        HStoreExtension(),

        migrations.CreateModel(
            name='DynamicField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(blank=True, help_text=b'The name that it is used internally, Leave it blank if you want the system to generate one for you.', max_length=255, unique=True)),
                ('type', models.CharField(choices=[(b'IntegerField', b'IntegerField'), (b'FloatField', b'FloatField'), (b'DecimalField', b'DecimalField'), (b'BooleanField', b'BooleanField'), (b'CharField', b'CharField'), (b'TextField', b'TextField'), (b'DateField', b'DateField'), (b'DateTimeField', b'DateTimeField'), (b'EmailField', b'EmailField'), (b'GenericIPAddressField', b'GenericIPAddressField'), (b'URLField', b'URLField')], max_length=30)),
                ('verbose_name', models.CharField(help_text=b'A human-readable name for the field.', max_length=255)),
                ('help_text', models.TextField(blank=True, help_text=b'Extra "help" text to be displayed with the form widget.')),
                ('default', models.CharField(blank=True, help_text=b'The default value for the field.', max_length=255, null=True)),
                ('blank', models.BooleanField(default=False, help_text=b'If True, the field is allowed to be blank.')),
                ('max_length', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('auto_now', models.BooleanField(default=False, help_text=b'Automatically set the field to now every time the object is saved.')),
                ('auto_now_add', models.BooleanField(default=False, help_text=b'Automatically set the field to now when the object is first created.')),
                ('max_digits', models.PositiveSmallIntegerField(blank=True, help_text=b'The maximum number of digits allowed in the number.Note that this number must be greater than or equal to decimal_places.', null=True)),
                ('decimal_places', models.PositiveSmallIntegerField(blank=True, help_text=b'The number of decimal places to store with the number.', null=True)),
                ('content_types', models.ManyToManyField(related_name='dynamic_fields', to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='DynamicFieldChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('dynamic_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='django_dynamic_fields.DynamicField')),
            ],
        ),
    ]
