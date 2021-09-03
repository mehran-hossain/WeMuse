import django_filters
from django.shortcuts import get_object_or_404
from django_filters import ChoiceFilter
from django.contrib.auth.models import User

from .models import Audio


class UserUploadFilter(django_filters.FilterSet):

    def __init__(self, data=None, *args, **kwargs):
        super(UserUploadFilter, self).__init__(data, *args, **kwargs)

    class Meta:
        model = Audio
        fields = {
        }
