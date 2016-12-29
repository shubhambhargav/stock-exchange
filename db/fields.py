import re
import json
from datetime import time, datetime

TYPE_ERROR_STRING = "Invalid %s value '%s' for %s: '%s'!"
CHOICE_ERROR_STRING = "Value '%s' not in choices '%s' for %s: %s!"

# Fields Definition
class Field(object):

    def __init__(self, inp=None, out=None, default=None, child=None, required=True):
        self.inp = inp
        self.out = out
        self.required = required
        self.default = default
        self.child = child

        self.validated_value = None

    def __str__(self):
        return '%s.%s.%s' % ('Field', self.inp, self.out)

    def __repr__(self):
        """
        Displays the module, class and name of the field.
        """
        path = '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        name = getattr(self, 'name', None)
        if name is not None:
            return '<%s: %s>' % (path, name)
        return '<%s>' % path

    def validate(self):
        return True


class IntField(Field):

    def validate(self, value):
        try:
            self.validated_value = int(value)
        except:
            raise TypeError(TYPE_ERROR_STRING % ("integer", value, self.__class__.__name__, self.inp))


class FloatField(Field):

    def validate(self, value):
        try:
            self.validated_value = float(value)
        except:
            raise TypeError(TYPE_ERROR_STRING % ("float", value, self.__class__.__name__, self.inp))


class CharField(Field):

    def validate(self, value):
        try:
            self.validated_value = str(value)
        except:
            raise TypeError(TYPE_ERROR_STRING % ("character", value, self.__class__.__name__, self.inp))


class TimeField(Field):

    def __init__(self, time_format='%H:%M:%S', **kwargs):
        super(TimeField, self).__init__(**kwargs)
        self.time_format = time_format

    def validate(self, value):
        if not isinstance(value, time):
            try:
                self.validated_value = datetime.strptime(value, self.time_format).time()
            except ValueError:
                raise TypeError(TYPE_ERROR_STRING % ("time", value, self.__class__.__name__, self.inp))
        else:
            self.validated_value = value


class ListField(Field):

    def validate(self, value):
        if type(value) != list:
            raise TypeError(TYPE_ERROR_STRING % ("list", value, self.__class__.__name__, self.inp))
        else:
            if self.child:
                child_instance = self.child()
                for v in value:
                    child_instance.validate(v)

            self.validated_value = value


class ChoiceField(Field):

    choice_field = ListField(inp="ChoiceField")

    def __init__(self, choices, **kwargs):
        super(ChoiceField, self).__init__(**kwargs)
        
        self.choice_field.validate(choices)
        self.choices = choices

    def validate(self, value):
        if value not in self.choices:
            raise ValueError(CHOICE_ERROR_STRING % (value, self.choices, self.__class__.__name__, self.inp))

        self.validated_value = value

