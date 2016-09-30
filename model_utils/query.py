from django.core.exceptions import ObjectDoesNotExist

def get_object(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist as e:
        return None
