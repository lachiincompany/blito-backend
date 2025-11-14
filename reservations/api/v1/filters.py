# filters.py
import django_filters
from reservations.models import Reservation

class ReservationFilter(django_filters.FilterSet):
    """فیلتر برای رزروها"""
    
    payment_status = django_filters.ChoiceFilter(
        choices=Reservation._meta.get_field('payment_status').choices,
        field_name='payment_status'
    )
    
    created_at_from = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='از تاریخ'
    )
    
    created_at_to = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='تا تاریخ'
    )
    
    total_price_min = django_filters.NumberFilter(
        field_name='total_price',
        lookup_expr='gte',
        label='حداقل قیمت'
    )
    
    total_price_max = django_filters.NumberFilter(
        field_name='total_price',
        lookup_expr='lte',
        label='حداکثر قیمت'
    )
    
    origin_city = django_filters.CharFilter(
        field_name='seat__trip__route__origin__city__name',
        lookup_expr='icontains',
        label='شهر مبدا'
    )
    
    destination_city = django_filters.CharFilter(
        field_name='seat__trip__route__destination__city__name',
        lookup_expr='icontains',
        label='شهر مقصد'
    )
    
    class Meta:
        model = Reservation
        fields = [
            'payment_status', 'created_at_from', 'created_at_to',
            'total_price_min', 'total_price_max', 'origin_city', 'destination_city'
        ]
