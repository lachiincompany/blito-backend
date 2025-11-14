# seats/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from seat.models import Seat
from seat.api.v1.serializers import (
    SeatSerializer, 
    SeatListSerializer, 
    SeatReservationSerializer
)
from trips.models import Trip

class SeatViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای مدیریت صندلی‌ها
    
    actions:
    - list: لیست تمام صندلی‌ها
    - retrieve: جزئیات یک صندلی
    - create: ایجاد صندلی جدید
    - update: ویرایش صندلی
    - destroy: حذف صندلی
    - reserve: رزرو صندلی
    - cancel_reservation: لغو رزرو
    - my_reservations: صندلی‌های رزرو شده توسط کاربر جاری
    - trip_seats: صندلی‌های یک سفر خاص
    """
    queryset = Seat.objects.select_related('trip', 'reserved_by').all()
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_reserved', 'trip', 'seat_number']
    search_fields = ['seat_number', 'reserved_by__first_name', 'reserved_by__last_name']
    ordering_fields = ['seat_number', 'reserved_at']
    ordering = ['seat_number']
    
    def get_serializer_class(self):
        """انتخاب سریالایزر مناسب بر اساس action"""
        if self.action == 'list':
            return SeatListSerializer
        elif self.action in ['reserve']:
            return SeatReservationSerializer
        return SeatSerializer
    
    def get_queryset(self):
        """فیلتر کردن بر اساس دسترسی کاربر"""
        queryset = super().get_queryset()
        
        # اگر کاربر عادی است، فقط صندلی‌های عمومی یا خودش را ببیند
        if not self.request.user.is_staff:
            # در اینجا می‌توانید منطق دسترسی خود را اضافه کنید
            pass
            
        return queryset
    
    @action(detail=False, methods=['post'])
    def reserve(self, request):
        """
        رزرو یک یا چند صندلی
        Body: {"seat_ids": [1, 2, 3]}
        """
        serializer = SeatReservationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        seat_ids = serializer.validated_data['seat_ids']
        
        try:
            with transaction.atomic():
                reserved_seats = []
                for seat_id in seat_ids:
                    seat = get_object_or_404(Seat, id=seat_id)
                    seat.reserve(request.user)
                    reserved_seats.append(seat)
                
                return Response({
                    'message': f'{len(reserved_seats)} صندلی با موفقیت رزرو شد',
                    'reserved_seats': SeatSerializer(reserved_seats, many=True).data
                }, status=status.HTTP_200_OK)
                
        except ValidationError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': 'خطا در رزرو صندلی'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def cancel_reservation(self, request, pk=None):
        """لغو رزرو یک صندلی"""
        seat = self.get_object()
        
        # بررسی اینکه کاربر مالک رزرو است یا ادمین
        if not request.user.is_staff and seat.reserved_by.user != request.user:
            return Response({
                'error': 'شما مجاز به لغو این رزرو نیستید'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            seat.cancel_reservation()
            return Response({
                'message': 'رزرو با موفقیت لغو شد'
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def my_reservations(self, request):
        """صندلی‌های رزرو شده توسط کاربر جاری"""
        if not hasattr(request.user, 'profile'):
            return Response({
                'error': 'لطفاً ابتدا پروفایل خود را تکمیل کنید'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        seats = self.get_queryset().filter(
            reserved_by=request.user.profile,
            is_reserved=True
        )
        
        serializer = SeatSerializer(seats, many=True)
        return Response({
            'count': seats.count(),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='trip/(?P<trip_id>[^/.]+)')
    def trip_seats(self, request, trip_id=None):
        """تمام صندلی‌های یک سفر"""
        trip = get_object_or_404(Trip, id=trip_id)
        seats = self.get_queryset().filter(trip=trip)
        
        # آمار صندلی‌ها
        total_seats = seats.count()
        reserved_seats = seats.filter(is_reserved=True).count()
        available_seats = total_seats - reserved_seats
        
        serializer = SeatListSerializer(seats, many=True)
        return Response({
            'trip_info': {
                'id': trip.id,
                'total_seats': total_seats,
                'reserved_seats': reserved_seats,
                'available_seats': available_seats
            },
            'seats': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def available_seats(self, request):
        """صندلی‌های در دسترس"""
        trip_id = request.query_params.get('trip')
        if not trip_id:
            return Response({
                'error': 'لطفاً ID سفر را مشخص کنید'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        seats = self.get_queryset().filter(
            trip_id=trip_id,
            is_reserved=False
        )
        
        serializer = SeatListSerializer(seats, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """ایجاد دسته‌ای صندلی برای یک سفر"""
        if not request.user.is_staff:
            return Response({
                'error': 'فقط ادمین‌ها مجاز به انجام این عمل هستند'
            }, status=status.HTTP_403_FORBIDDEN)
        
        trip_id = request.data.get('trip_id')
        if not trip_id:
            return Response({
                'error': 'لطفاً ID سفر را مشخص کنید'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        trip = get_object_or_404(Trip, id=trip_id)
        
        try:
            with transaction.atomic():
                seats = []
                for i in range(1, trip.bus.capacity + 1):
                    seat, created = Seat.objects.get_or_create(
                        trip=trip,
                        seat_number=i
                    )
                    if created:
                        seats.append(seat)
                
                return Response({
                    'message': f'{len(seats)} صندلی جدید ایجاد شد',
                    'created_seats': len(seats)
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'error': 'خطا در ایجاد صندلی‌ها'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)