from django.db.models.signals import post_save, post_delete, pre_delete, m2m_changed
from django.dispatch import receiver
from django_dynamic_fields.models import DynamicField
from django_dynamic_fields.utils import update_schemas


@receiver(pre_delete, sender=DynamicField)
def dynamic_field_model_pre_delete(sender, instance, **kwargs):
    for content_type in instance.content_types.all():
        print content_type
        model = content_type.model_class()
        model.objects.all().hremove('hstore_data', instance.field_name)


@receiver(post_delete, sender=DynamicField)
def dynamic_field_model_post_delete(sender, instance, **kwargs):
    for content_type in instance.content_types.all():
        model = content_type.model_class()
        model.objects.all().hremove('hstore_data', instance.field_name)
    update_schemas()


@receiver(post_save, sender=DynamicField)
def dynamic_field_model_post_save(sender, instance, **kwargs):
    update_schemas()


@receiver(m2m_changed, sender=DynamicField.content_types.through)
def dynamic_field_model_through(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        update_schemas()
