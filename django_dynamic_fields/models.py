from decimal import Decimal

from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import curry
from django_hstore import hstore


class HstoreModel(models.Model):
    hstore_data = hstore.DictionaryField(null=True, editable=False)
    objects = hstore.HStoreManager()

    class Meta:
        abstract = True

    @classmethod
    def update_schema(cls):
        ct = ContentType.objects.get(app_label=cls._meta.app_label, model=cls._meta.model_name)
        fields = ct.dynamic_fields.all()
        schema = [field.get_schema() for field in fields]
        cls._meta.get_field('hstore_data').reload_schema(schema)
        cls.contribute()

    @classmethod
    def contribute(cls):
        ct = ContentType.objects.get(app_label=cls._meta.app_label, model=cls._meta.model_name)
        fields = ct.dynamic_fields.all()
        for field in fields:
            virtual_field = cls._meta.get_field(field.field_name)
            if field.get_choices():
                setattr(
                    cls, 'get_%s_display' % virtual_field.attname,
                    curry(cls._get_FIELD_display, field=virtual_field)
                )


FIELD_TYPE_CHOICES = (
    ('IntegerField', 'IntegerField'),
    ('FloatField', 'FloatField'),
    ('DecimalField', 'DecimalField'),
    ('BooleanField', 'BooleanField'),
    ('CharField', 'CharField'),
    ('TextField', 'TextField'),
    ('DateField', 'DateField'),
    ('DateTimeField', 'DateTimeField'),
    ('EmailField', 'EmailField'),
    ('GenericIPAddressField', 'GenericIPAddressField'),
    ('URLField', 'URLField'),
)


class DynamicField(models.Model):
    content_types = models.ManyToManyField(ContentType, related_name='dynamic_fields')
    field_name = models.CharField(
        max_length=255, blank=True, unique=True,
        help_text='The name that it is used internally, Leave it blank if you want the system to generate one for you.'
    )

    type = models.CharField(max_length=30, choices=FIELD_TYPE_CHOICES)

    verbose_name = models.CharField(max_length=255, help_text='A human-readable name for the field.')
    help_text = models.TextField(blank=True, help_text='Extra "help" text to be displayed with the form widget.')
    default = models.CharField(max_length=255, blank=True, null=True, help_text='The default value for the field.')
    blank = models.BooleanField(default=False, help_text='If True, the field is allowed to be blank.')

    max_length = models.PositiveSmallIntegerField(blank=True, null=True)

    auto_now = models.BooleanField(
        default=False, help_text='Automatically set the field to now every time the object is saved.'
    )
    auto_now_add = models.BooleanField(
        default=False, help_text='Automatically set the field to now when the object is first created.'
    )

    max_digits = models.PositiveSmallIntegerField(
        blank=True, null=True,
        help_text='The maximum number of digits allowed in the number.'
                  'Note that this number must be greater than or equal to decimal_places.'
    )
    decimal_places = models.PositiveSmallIntegerField(
        blank=True, null=True, help_text='The number of decimal places to store with the number.'
    )

    def save(self, *args, **kwargs):
        if not self.field_name:
            self.field_name = self._generate_field_name()
        super(DynamicField, self).save(*args, **kwargs)


    def __unicode__(self):
        return u'%s' % self.verbose_name

    def get_choices(self):
        choice_list = [(choice.id, choice.name) for choice in self.choices.all()]
        return tuple(choice_list)

    def _generate_field_name(self):
        try:
            last_id = DynamicField.objects.latest('id').id
        except DynamicField.DoesNotExist:
            last_id = 0
        return '%s_%s' % (slugify(self.type), last_id + 1)

    def _get_default(self):
        field_type = self.type
        if self.default:
            if field_type == 'IntegerField':
                return int(self.default)
            elif field_type == 'FloatField':
                return float(self.default)
            elif field_type == 'DecimalField':
                return Decimal(self.default)
            elif field_type == 'BooleanField':
                return self.default not in ('False', 'false', 'No', 'no', '0')
            else:
                return self.default
        else:
            return None

    def _get_field_kwargs(self):
        kwargs = {}
        if self.verbose_name:
            kwargs['verbose_name'] = self.verbose_name
        if self.help_text:
            kwargs['help_text'] = self.help_text
        if self.default is not None:
            kwargs['default'] = self._get_default()
        if self.blank:
            kwargs['blank'] = True

        if self.max_length is not None:
            kwargs['max_length'] = self.max_length

        if self.auto_now:
            kwargs['auto_now'] = True
        if self.auto_now_add:
            kwargs['auto_now_add'] = True

        if self.max_digits is not None:
            kwargs['max_digits'] = self.max_digits
        if self.decimal_places is not None:
            kwargs['decimal_places'] = self.decimal_places

        if self.choices.exists():
            kwargs['choices'] = self.get_choices()
        return kwargs

    def _get_field_type(self):
        if self.choices.exists():
            return 'IntegerField'
        else:
            return self.type

    def get_schema(self):
        return {
            'name': self.field_name,
            'class': self._get_field_type(),
            'kwargs': self._get_field_kwargs()
        }


class DynamicFieldChoice(models.Model):
    dynamic_field = models.ForeignKey(DynamicField, related_name="choices")
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % self.name
