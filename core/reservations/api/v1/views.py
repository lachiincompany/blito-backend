# views.py
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from reservations.models import Reservation
from .serializers import (
    ReservationListSerializer, 
    ReservationDetailSerializer,
    ReservationCreateSerializer,
    ReservationUpdateSerializer
)
from reservations.api.v1.filters import ReservationFilter
from reservations.api.v1.permissions import IsOwnerOrAdmin
from rest_framework import serializers

class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای مدیریت رزروها
    
    - list: نمایش لیست رزروها (فقط رزروهای خود کاربر)
    - create: ایجاد رزرو جدید
    - retrieve: نمایش جزئیات رزرو
    - update: بروزرسانی وضعیت پرداخت
    - destroy: حذف رزرو (فقط رزروهای در انتظار پرداخت)
    """
    
    queryset = Reservation.objects.select_related(
        'seat__trip__route__origin__city',
        'seat__trip__route__destination__city',
        'seat__trip__route__company',
        'seat__trip__bus',
        'user__user'
    ).all()
    
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ReservationFilter
    search_fields = ['reservation_code', 'user__user__phone', 'user__first_name', 'user__last_name']
    ordering_fields = ['created_at', 'total_price', 'payment_status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """انتخاب سریالایزر مناسب بر اساس action"""
        if self.action == 'list':
            return ReservationListSerializer
        elif self.action == 'create':
            return ReservationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ReservationUpdateSerializer
        return ReservationDetailSerializer
    
    def get_queryset(self):
        """فیلتر کردن رزروها بر اساس کاربر"""
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return self.queryset
        # نمایش فقط رزروهای خود کاربر
        return self.queryset.filter(user__user=user)
    
    def perform_create(self, serializer):
        """تنظیم کاربر هنگام ایجاد رزرو"""
        # فرض بر این است که کاربر Profile دارد
        profile = getattr(self.request.user, 'profile', None)
        if not profile:
            raise serializers.ValidationError("پروفایل کاربری یافت نشد.")
        serializer.save(user=profile)
    
    def destroy(self, request, *args, **kwargs):
        """حذف رزرو - فقط رزروهای در انتظار پرداخت"""
        reservation = self.get_object()
        if reservation.payment_status != 'PENDING':
            return Response(
                {'detail': 'فقط رزروهای در انتظار پرداخت قابل حذف هستند.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        """تایید پرداخت رزرو"""
        reservation = self.get_object()
        if reservation.payment_status != 'PENDING':
            return Response(
                {'detail': 'این رزرو قابل تایید پرداخت نیست.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservation.payment_status = 'PAID'
        reservation.save()
        
        serializer = self.get_serializer(reservation)
        return Response(
            {'detail': 'پرداخت با موفقیت تایید شد.', 'reservation': serializer.data},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def cancel_reservation(self, request, pk=None):
        """لغو رزرو"""
        reservation = self.get_object()
        if reservation.payment_status == 'PAID':
            return Response(
                {'detail': 'رزروهای پرداخت شده قابل لغو نیستند.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservation.payment_status = 'FAILED'
        reservation.save()
        
        return Response(
            {'detail': 'رزرو با موفقیت لغو شد.'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def my_reservations(self, request):
        """رزروهای کاربر جاری"""
        queryset = self.get_queryset().filter(user__user=request.user)
        serializer = ReservationListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """آمار رزروها برای ادمین"""
        if not request.user.is_staff:
            return Response(
                {'detail': 'دسترسی غیرمجاز.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        total_reservations = self.get_queryset().count()
        paid_reservations = self.get_queryset().filter(payment_status='PAID').count()
        pending_reservations = self.get_queryset().filter(payment_status='PENDING').count()
        failed_reservations = self.get_queryset().filter(payment_status='FAILED').count()
        
        return Response({
            'total_reservations': total_reservations,
            'paid_reservations': paid_reservations,
            'pending_reservations': pending_reservations,
            'failed_reservations': failed_reservations,
            'success_rate': f"{(paid_reservations/total_reservations*100):.2f}%" if total_reservations > 0 else "0%"
        })
