import string
from django.contrib import admin
from django_dynamic_fields.forms import ExtraFieldAdminForm
from django_dynamic_fields.models import DynamicFieldChoice, DynamicField


class ExtraFieldChoiceInline(admin.TabularInline):
    model = DynamicFieldChoice
    extra = 0


class ExtraFieldInline(admin.ModelAdmin):
    model = DynamicField
    list_display = ['verbose_name', 'get_models']
    fieldsets = (
        (None, {
            'fields': (
                'content_types', 'type', 'verbose_name',
            )
        }),
        ('Optional', {
            'fields': (
                'help_text', 'default', 'field_name',
            )
        }),
        ('CharField or TextField options', {
            'classes': ('collapse',),
            'fields': ('max_length',)
        }),
        ('DateField or DateTimeField options', {
            'classes': ('collapse',),
            'fields': ('auto_now', 'auto_now_add',)
        }),
        ('DecimalField options', {
            'classes': ('collapse',),
            'fields': ('max_digits', 'decimal_places',)
        }),
    )
    filter_horizontal = ['content_types', ]
    inlines = [ExtraFieldChoiceInline, ]
    form = ExtraFieldAdminForm

    def get_models(self, obj):
        return ", ".join([string.capwords(p.name) for p in obj.content_types.all()])
    get_models.short_description = 'Models'

    def get_description(self, obj):
        return ", ".join([p.name for p in obj.choices.all()])
    get_description.short_description = 'Fields'


admin.site.register(DynamicField, ExtraFieldInline)
