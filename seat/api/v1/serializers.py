
# seats/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from seat.models import Seat
from trips.api.v1.serializers import TripSerializer 
from accounts.api.v1.serializers import ProfileSerializer

User = get_user_model()

class PassengerInfoSerializer(serializers.Serializer):
    """سریالایزر برای نمایش اطلاعات مسافر"""
    name = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    national_id = serializers.CharField(read_only=True)

class SeatSerializer(serializers.ModelSerializer):
    passenger_info = PassengerInfoSerializer(read_only=True)
    trip_details = TripSerializer(source='trip', read_only=True)
    reserved_by_details = ProfileSerializer(source='reserved_by', read_only=True)
    can_cancel = serializers.SerializerMethodField()
    
    class Meta:
        model = Seat
        fields = [
            'id', 'trip', 'seat_number', 'is_reserved', 
            'reserved_by', 'reserved_at', 'passenger_info',
            'trip_details', 'reserved_by_details', 'can_cancel'
        ]
        read_only_fields = ['is_reserved', 'reserved_by', 'reserved_at']
    
    def get_can_cancel(self, obj):
        """بررسی امکان لغو رزرو"""
        if not obj.is_reserved:
            return False
        return obj.trip.can_cancel if hasattr(obj.trip, 'can_cancel') else True

class SeatListSerializer(serializers.ModelSerializer):
    """سریالایزر ساده برای لیست صندلی‌ها"""
    passenger_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'is_reserved', 'passenger_name', 'reserved_at']
    
    def get_passenger_name(self, obj):
        if obj.passenger_info:
            return obj.passenger_info.get('name')
        return None

class SeatReservationSerializer(serializers.Serializer):
    """سریالایزر برای رزرو صندلی"""
    seat_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="لیست ID صندلی‌های مورد نظر برای رزرو"
    )