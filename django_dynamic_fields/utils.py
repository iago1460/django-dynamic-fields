def update_schemas():
    from django.contrib.contenttypes.models import ContentType
    models = ContentType.objects.filter(dynamic_fields__isnull=False).distinct()
    for model in models:
        target_model = model.model_class()
        target_model.update_schema()
