
# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from reservations.models import Reservation
from seat.models import Seat
from seat.api.v1.serializers import SeatSerializer 

User = get_user_model()

class PassengerInfoSerializer(serializers.Serializer):
    """سریالایزر برای اطلاعات مسافر"""
    name = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    national_id = serializers.CharField(read_only=True, required=False)
    full_name = serializers.CharField(read_only=True)

class TripInfoSerializer(serializers.Serializer):
    """سریالایزر برای اطلاعات سفر"""
    origin = serializers.CharField(read_only=True)
    destination = serializers.CharField(read_only=True)
    departure_datetime = serializers.DateTimeField(read_only=True)
    company = serializers.CharField(read_only=True)
    bus_type = serializers.CharField(read_only=True)
    seat_number = serializers.CharField(read_only=True)

class ReservationListSerializer(serializers.ModelSerializer):
    """سریالایزر برای نمایش لیست رزروها"""
    passenger_info = PassengerInfoSerializer(read_only=True)
    trip_info = TripInfoSerializer(read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'reservation_code', 'total_price', 'payment_status', 
            'payment_status_display', 'created_at', 'passenger_info', 'trip_info'
        ]
        read_only_fields = ['id', 'reservation_code', 'created_at']

class ReservationDetailSerializer(serializers.ModelSerializer):
    """سریالایزر برای جزئیات رزرو"""
    passenger_info = PassengerInfoSerializer(read_only=True)
    trip_info = TripInfoSerializer(read_only=True)
    seat_details = SeatSerializer(source='seat', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'reservation_code', 'seat', 'user', 'total_price', 
            'payment_status', 'payment_status_display', 'created_at',
            'passenger_info', 'trip_info', 'seat_details'
        ]
        read_only_fields = ['id', 'reservation_code', 'created_at']

class ReservationCreateSerializer(serializers.ModelSerializer):
    """سریالایزر برای ایجاد رزرو جدید"""
    
    class Meta:
        model = Reservation
        fields = ['seat', 'user', 'total_price']
        
    def validate_seat(self, value):
        """بررسی در دسترس بودن صندلی"""
        if Reservation.objects.filter(seat=value, payment_status__in=['PENDING', 'PAID']).exists():
            raise serializers.ValidationError("این صندلی قبلاً رزرو شده است.")
        return value
    
    def validate_total_price(self, value):
        """بررسی صحت قیمت"""
        if value <= 0:
            raise serializers.ValidationError("قیمت باید مثبت باشد.")
        return value

class ReservationUpdateSerializer(serializers.ModelSerializer):
    """سریالایزر برای بروزرسانی وضعیت پرداخت"""
    
    class Meta:
        model = Reservation
        fields = ['payment_status']
        
    def validate_payment_status(self, value):
        """بررسی صحت تغییر وضعیت پرداخت"""
        instance = self.instance
        if instance.payment_status == 'PAID' and value != 'REFUNDED':
            raise serializers.ValidationError("فقط می‌توان رزرو پرداخت شده را به حالت برگشت داده شده تغییر داد.")
        return value