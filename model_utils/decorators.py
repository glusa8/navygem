from functools import wraps
from django.utils import timezone
from model_utils.choices import Choices


def stringify(arr):
    return [str(elem) for elem in arr]

def validate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        obj = args[0]
        getattr(
            obj.validator,
            'validate_{}'.format(func.__name__)
        )(obj)
        return func(*args, **kwargs)
    return wrapper


def post_validate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        obj = args[0]
        func_name = func.__name__[len('set_'):]
        result = func(*args, **kwargs)
        getattr(
            obj.validator,
            'validate_{}'.format(func_name)
        )(obj)
        return result
    return wrapper

def auto_add_time_deleted(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        obj = args[0]
        if (
            hasattr(obj, 'is_deleted') and
            hasattr(obj, 'time_deleted')
        ):
            if (
                obj.is_deleted and
                obj.time_deleted is None
            ):
                obj.time_deleted = timezone.now()
            elif (
                not obj.is_deleted and
                obj.time_deleted is not None
            ):
                obj.time_deleted = None

        return func(*args, **kwargs)
    return wrapper

def auto_add_time_deactivated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        obj = args[0]
        if (
            hasattr(obj, 'is_deactivated') and
            hasattr(obj, 'time_deactivated')
        ):
            if (
                obj.is_deactivated and
                obj.time_deactivated is None
            ):
                obj.time_deactivated = timezone.now()
            elif (
                not obj.is_deactivated and
                obj.time_deactivated is not None
            ):
                obj.time_deactivated = None

        return func(*args, **kwargs)
    return wrapper

def enforce_choice_selections(choice_labels):
    def func_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            obj = args[0]
            for choice_label in choice_labels:
                # Just have to check whether
                # getattr(obj, choice_label) is not None.
                # If a CharField is not None-able, but is set to None,
                # Django will throw an error.
                if (
                    hasattr(obj, choice_label) and
                    getattr(obj, choice_label) is not None and
                    hasattr(obj, '{}_choices'.format(choice_label)) and
                    isinstance(getattr(obj, '{}_choices'.format(choice_label)), Choices)
                ):
                    choice = getattr(obj, choice_label)
                    choices = [
                        c[0]
                        for c
                        in getattr(obj, '{}_choices'.format(choice_label)).all()
                    ]
                    if choice not in choices:
                        raise Exception(
                            'The {} field has a value "{}" that is not one of the allowed choices: {}'.format(
                                choice_label,
                                choice,
                                stringify(choices)
                            )
                        )

            return func(*args, **kwargs)
        return wrapper
    return func_wrapper

def enforce_date_time_order(date_time_labels):
    def func_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            obj = args[0]
            date_times = []
            for (index, date_time_label) in enumerate(date_time_labels):
                if hasattr(obj, date_time_label):
                    date_times.append(
                        (date_time_label, getattr(obj, date_time_label))
                    )

            first_none_date_time_label = None
            first_none_date_time_label_index = -1
            for (index, (date_time_label, date_time)) in enumerate(date_times):
                if date_time is None:
                    first_none_date_time_label = date_time_label
                    first_none_date_time_label_index = index
                    break

            if first_none_date_time_label_index != -1:
                for (date_time_label, date_time) in date_times[index + 1:]:
                    if date_time is not None:
                        raise Exception(
                            'The date time field "{}" cannot be set when another field "{}" is None. The order of which date time must be set first from left to right: {}'.format(
                                date_time_label,
                                first_none_date_time_label,
                                stringify(date_time_labels)
                            )
                        )

            for (index, (date_time_label, date_time)) in enumerate(date_times):
                if date_time is None:
                    break
                if index == 0:
                    continue
                (prev_date_time_label, prev_date_time) = date_times[index - 1]
                if date_time < prev_date_time:
                    raise Exception(
                        'The date time field "{}" cannot be set earlier than another field "{}." The order is: {}'.format(
                            date_time_label,
                            prev_date_time_label,
                            ' < '.join(date_time_labels)
                        )
                    )

            return func(*args, **kwargs)
        return wrapper
    return func_wrapper
