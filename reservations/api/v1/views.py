# views.py
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
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
    مدیریت رزرو بلیط‌ها برای کاربران سیستم.

    این ویوست تمام عملیات اصلی مربوط به رزرو را پوشش می‌دهد:

    - **GET /reservations/api/v1/api/reservations/**: لیست رزروهای کاربر جاری  
    - **POST /reservations/api/v1/api/reservations/**: ایجاد رزرو جدید برای یک صندلی مشخص  
    - **GET /reservations/api/v1/api/reservations/{id}/**: مشاهده جزئیات یک رزرو  
    - **DELETE /reservations/api/v1/api/reservations/{id}/**: حذف رزرو *فقط اگر در حالت «در انتظار پرداخت» باشد*  

    دسترسی‌ها:
    - کاربر معمولی فقط رزروهای خودش را می‌بیند.
    - ادمین می‌تواند تمام رزروها را مشاهده و مدیریت کند.
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
        """
        انتخاب سریالایزر مناسب بر اساس اکشن فعلی.

        - list → `ReservationListSerializer`
        - create → `ReservationCreateSerializer`
        - update / partial_update → `ReservationUpdateSerializer`
        - سایر اکشن‌ها → `ReservationDetailSerializer`
        """
        if self.action == 'list':
            return ReservationListSerializer
        elif self.action == 'create':
            return ReservationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ReservationUpdateSerializer
        return ReservationDetailSerializer
    
    def get_queryset(self):
        """
        فیلتر کردن رزروها بر اساس نقش و کاربر جاری.

        - اگر کاربر ادمین باشد، تمام رزروها را می‌بیند.
        - اگر کاربر معمولی باشد، فقط رزروهای مربوط به خودش را می‌بیند.
        """
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return qs
        # نمایش فقط رزروهای خود کاربر
        return qs.filter(user__user=user)
    
    def perform_create(self, serializer):
        """
        هنگام ایجاد رزرو جدید، پروفایل کاربر جاری به عنوان مسافر روی رزرو تنظیم می‌شود.

        نکته:
        - برای ایجاد رزرو، لازم است کاربر پروفایل تکمیل‌شده (Profile) داشته باشد.
        """
        # فرض بر این است که کاربر Profile دارد
        profile = getattr(self.request.user, 'profile', None)
        if not profile:
            raise serializers.ValidationError("پروفایل کاربری یافت نشد.")
        serializer.save(user=profile)
    
    def destroy(self, request, *args, **kwargs):
        """
        حذف رزرو.

        محدودیت:
        - فقط رزروهایی که در وضعیت `PENDING` (در انتظار پرداخت) هستند قابل حذف‌اند.
        - در صورت حذف، صندلی مرتبط نیز آزاد می‌شود.
        """
        reservation = self.get_object()
        if reservation.payment_status != Reservation.PaymentStatus.PENDING:
            return Response(
                {'detail': 'فقط رزروهای در انتظار پرداخت قابل حذف هستند.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        reservation.release_seat()
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        """
        تایید پرداخت یک رزرو به صورت دستی.

        استفاده معمول زمانی است که پرداخت از طریق سیستم دیگری انجام شده
        و شما می‌خواهید وضعیت رزرو را به صورت دستی روی «پرداخت‌شده» قرار دهید.

        اثرات:
        - وضعیت رزرو به `PAID` تغییر می‌کند.
        - صندلی رزرو شده در حالت رزروشده باقی می‌ماند.
        """
        reservation = self.get_object()
        if reservation.payment_status != Reservation.PaymentStatus.PENDING:
            return Response(
                {'detail': 'این رزرو قابل تایید پرداخت نیست.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.mark_as_paid()

        serializer = self.get_serializer(reservation)
        return Response(
            {'detail': 'پرداخت با موفقیت تایید شد.', 'reservation': serializer.data},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def cancel_reservation(self, request, pk=None):
        """
        لغو یک رزرو توسط کاربر یا ادمین.

        محدودیت‌ها:
        - رزروهایی که در وضعیت `PAID` هستند قابل لغو نیستند.

        اثرات:
        - وضعیت رزرو به `FAILED` تغییر می‌کند.
        - صندلی مربوطه آزاد می‌شود.
        """
        reservation = self.get_object()
        if reservation.payment_status == Reservation.PaymentStatus.PAID:
            return Response(
                {'detail': 'رزروهای پرداخت شده قابل لغو نیستند.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.mark_as_failed()

        return Response(
            {'detail': 'رزرو با موفقیت لغو شد.'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def my_reservations(self, request):
        """
        لیست تمام رزروهای کاربر جاری.

        این اکشن مشابه لیست معمول است اما به صورت صریح فقط رزروهای
        مرتبط با کاربر لاگین‌شده را برمی‌گرداند و برای استفاده در فرانت‌اند
        (مثلاً صفحه «رزروهای من») مناسب است.
        """
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
