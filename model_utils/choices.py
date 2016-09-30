import math
import string

class Choices(object):

    class ChoiceIterator(object):
        def __init__(self, choices):
            self._iterable = list(choices.all())

        def next(self):
            if len(self._iterable) > 0:
                return self._iterable.pop(0)[0]
            else:
                raise StopIteration

    def __init__(self, choices, default=None):
        if len(choices) == 0:
            raise Exception('Must provide at least one choice')

        is_tuple = type(choices[0]) == tuple

        for c in choices:
            if (
                (is_tuple and type(c) != tuple) or
                (not is_tuple and type(c) == tuple)
            ):
                raise Exception('All choices must be either tuples or strings')

        allowed_letters = set(string.ascii_lowercase + '_')

        for c in choices:
            c_tuple = c if is_tuple else (c,)

            for member in c_tuple:
                for l in member:
                    if l not in allowed_letters:
                        raise Exception(
                            'A choice can only be any lowercase alphabetical letter or "_": {}'.format(member)
                        )

        self._choices = [
            (c, c)
            if not is_tuple
            else (c[0], c[1])
            for c in choices
        ]

        choice_descriptions = [c[1] for c in self._choices]

        if default is not None:
            if default not in choice_descriptions:
                raise Exception(
                    'Default "{}" is not one of the choices: {}'.format(
                        default,
                        self._choices
                    )
                )

            index = choice_descriptions.index(default)

            self._default = self._choices[index][0]
        else:
            self._default = None

        for c in self._choices:
            setattr(self, c[1].upper(), c[0])

    def __iter__(self):
        return self.ChoiceIterator(self)

    def all(self):
        return list(self._choices)

    def default(self):
        if self._default is None:
            raise Exception('There is no default for this Choices object')
        return self._default

    def from_description(self, desc):
        for c in self._choices:
            if desc == c[1]:
                return c[0]

    def to_description(self, choice):
        for c in self._choices:
            if choice == c[0]:
                return c[1]

class Bitmap(object):

    class BitmapIterator(object):

        def __init__(self, bitmap):
            self._iterable = list(sorted(bitmap._bitmap.values()))

        def next(self):
            if len(self._iterable) > 0:
                return self._iterable.pop(0)
            else:
                raise StopIteration

    def __init__(self, choices, default_choices=None):
        if default_choices is None:
            default_choices = []

        if len(choices) == 0:
            raise Exception('Must provide at least one choice')

        allowed_letters = set(string.ascii_lowercase + '_')

        for c in choices:
            for l in c:
                if l not in allowed_letters:
                    raise Exception(
                        'A choice can only be any lowercase alphabetical letter or "_": {}'.format(c)
                    )

        self._bitmap = dict((c, int(math.pow(2, i))) for (i, c) in enumerate(choices))

        if len(default_choices) != 0:
            for c in default_choices:
                if c not in choices:
                    raise Exception(
                        'Choice "{}" is not one of the choices: {}'.format(
                            c,
                            choices
                        )
                    )

            default_code = 0
            for c in default_choices:
                default_code |= self._bitmap[c]

            self._default_code = default_code
        else:
            self._default_code = None

        for (k, v) in self._bitmap.items():
            setattr(self, k.upper(), v)

    def __iter__(self):
        return self.BitmapIterator(self)

    def decode(self, code):
        choices = []
        for (k, v) in sorted(self._bitmap.items(), key=lambda x: x[1]):
            if v & code != 0:
                choices.append(k)
        return choices

    def encode(self, choice_codes):
        code = 0
        for (_, v) in self._bitmap.items():
            for cc in choice_codes:
                if cc == v:
                    code |= v
        return code

    def all(self):
        return sorted([v for (_, v) in self._bitmap.items()])

    def default_code(self):
        if self._default_code is None:
            raise Exception('There is no default_code for this Bitmap object')
        return self._default_code
