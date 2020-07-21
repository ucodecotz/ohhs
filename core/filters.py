import django_filters
from django.contrib.auth.models import User
from django.forms.widgets import CheckboxSelectMultiple

from .models import *
from django.conf import settings
from django_filters.filters import ChoiceFilter

RELIGION = (
    ('MU', 'Muslims'),
    ('CH', 'Christianity'),
)
TRIBE = (
    ('HY', 'Haya'),
    ('SK', 'Sukluma'),
)


class laboursFilterForm(django_filters.FilterSet):
    user = django_filters.ModelMultipleChoiceFilter(
        queryset=User.objects.all(),
        widget=CheckboxSelectMultiple(),
        label="User",
        label_suffix="",
    )
    religion = django_filters.ChoiceFilter(choices=RELIGION)

    class Meta:
        model = LaboursProfile
        fields = ['religion', 'user', 'tribe', 'work']
