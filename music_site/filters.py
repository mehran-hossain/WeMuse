import django_filters
from django_filters import ChoiceFilter
from musix.models import Audio


class AudioFilter(django_filters.FilterSet):
    uploader = django_filters.CharFilter(field_name='uploader__username', lookup_expr='icontains', label='Uploaded by')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label="Title")
    genre = django_filters.CharFilter(field_name='genre', lookup_expr='icontains', label="Genre")
    key = django_filters.CharFilter(field_name='key', lookup_expr='icontains', label="Key")
    instrument = django_filters.CharFilter(field_name='instrument', lookup_expr='icontains', label="Instrument")
    # order_by = django_filters.OrderingFilter(fields=('sample_count',), label='Times used')

    class Meta:
        model = Audio
        fields = {
        }
