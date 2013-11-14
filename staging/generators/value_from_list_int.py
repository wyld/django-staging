import random
from django.db import models
from django import forms
from staging.generators import BaseGenerator


class ValueFromListForm(forms.Form):
    lines = forms.CharField(widget=forms.Textarea)


class NotInitialized():
    pass


class Generator(BaseGenerator):
    name = 'Value from list'
    slug = 'value-from-list-int'
    for_fields = [models.BigIntegerField, models.DecimalField, models.IntegerField, models.PositiveIntegerField,
                  models.PositiveSmallIntegerField, models.SmallIntegerField]
    options_form = ValueFromListForm

    def __init__(self):
        self.lines_left = NotInitialized

    def save(self, obj, field, form_data):
        if field.unique:
            if self.lines_left == NotInitialized:
                self.lines_left = form_data.get('lines').split('\n')
            setattr(obj, field.name, self._generate_unique())
        else:
            setattr(obj, field.name, self._generate(form_data.get('lines')))

    def _generate(self, text):
        lines = text.split('\n')
        return int(random.choice(lines))

    def _generate_unique(self):
        if self.lines_left:
            value = int(random.choice(self.lines_left))
            self.lines_left = [x for x in self.lines_left if x != value]
            return value
