from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from payments.models import Payment
from .serializers import (
    PaymentListSerializer,
    PaymentDetailSerializer,
    PaymentCreateSerializer,
    PaymentStatusSerializer,
    PaymentRefundSerializer,
)
from .permissions import IsPaymentOwnerOrAdmin


class PaymentViewSet(viewsets.ModelViewSet):
    """
    مدیریت تراکنش‌های پرداخت مرتبط با رزروها.

    سناریوی معمول:
    1. کاربر ابتدا یک رزرو ایجاد می‌کند.
    2. سپس با استفاده از این ویوست برای آن رزرو یک پرداخت ثبت می‌کند.
    3. در منطق فعلی، پرداخت بلافاصله به صورت داخلی «موفق» می‌شود و
       وضعیت رزرو به `PAID` تغییر می‌کند (بدون رفتن به درگاه بانکی واقعی).

    اندپوینت‌های مهم:
    - **GET /payments/api/v1/api/payments/**: لیست پرداخت‌های کاربر جاری یا همه (برای ادمین)
    - **POST /payments/api/v1/api/payments/**: ایجاد پرداخت جدید برای یک رزرو
    - **GET /payments/api/v1/api/payments/{id}/**: جزییات یک پرداخت به همراه اطلاعات رزرو
    - **POST /payments/api/v1/api/payments/{id}/process/**: بروزرسانی وضعیت پرداخت (در حالت اتصال به درگاه)
    - **POST /payments/api/v1/api/payments/{id}/refund/**: برگشت مبلغ پرداخت (ادمین)
    """
    queryset = Payment.objects.select_related(
        'reservation__seat__trip__route__origin__city',
        'reservation__seat__trip__route__destination__city',
        'reservation__user__user',
    ).all()
    permission_classes = [IsAuthenticated, IsPaymentOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'gateway']
    search_fields = ['authority', 'reference_id', 'reservation__reservation_code']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        انتخاب سریالایزر بر اساس نوع اکشن:

        - list → `PaymentListSerializer`
        - create → `PaymentCreateSerializer`
        - سایر اکشن‌ها → `PaymentDetailSerializer`
        """
        if self.action == 'list':
            return PaymentListSerializer
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentDetailSerializer

    def get_queryset(self):
        """
        بازگرداندن لیست پرداخت‌ها بر اساس نقش کاربر:

        - ادمین: مشاهده تمام پرداخت‌ها
        - کاربر معمولی: فقط پرداخت‌های مربوط به رزروهای خودش
        """
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return qs
        return qs.filter(reservation__user__user=user)

    @action(detail=True, methods=['post'], url_path='process')
    def process_payment(self, request, pk=None):
        """
        بروزرسانی وضعیت یک پرداخت (سناریوی اتصال به درگاه واقعی).

        در منطق فعلی شما می‌توانید از این اکشن زمانی استفاده کنید
        که درگاه بانکی پس از بازگشت، نتیجه را به شما اطلاع می‌دهد.

        بدنه درخواست (مثال):
        ```json
        {
          "success": true,
          "reference_id": "BANK-REF-123",
          "metadata": {"bank": "demo"}
        }
        ```
        """
        payment = self.get_object()
        serializer = PaymentStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if payment.status not in [Payment.Status.INITIATED, Payment.Status.PROCESSING]:
            return Response(
                {'detail': 'وضعیت این پرداخت قابل تغییر نیست.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.validated_data['success']:
            payment.mark_success(
                reference_id=serializer.validated_data.get('reference_id'),
                metadata=serializer.validated_data.get('metadata'),
            )
            message = 'پرداخت با موفقیت تایید شد.'
        else:
            payment.mark_failed(metadata=serializer.validated_data.get('metadata'))
            message = 'پرداخت ناموفق ثبت شد.'

        detail_serializer = PaymentDetailSerializer(payment, context={'request': request})
        return Response({'detail': message, 'payment': detail_serializer.data})

    @action(detail=True, methods=['post'], url_path='refund')
    def refund_payment(self, request, pk=None):
        """
        برگشت مبلغ پرداخت (Refund) – فقط برای ادمین.

        محدودیت:
        - فقط پرداخت‌هایی که در وضعیت `SUCCESS` هستند قابل برگشت‌اند.

        اثرات:
        - وضعیت Payment به `REFUNDED` تغییر می‌کند.
        - وضعیت رزرو مرتبط نیز به حالت برگشت‌داده‌شده تنظیم می‌شود.
        """
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({'detail': 'دسترسی غیرمجاز.'}, status=status.HTTP_403_FORBIDDEN)

        payment = self.get_object()
        if payment.status != Payment.Status.SUCCESS:
            return Response(
                {'detail': 'فقط پرداخت‌های موفق قابل برگشت هستند.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PaymentRefundSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment.mark_refunded(metadata=serializer.validated_data.get('metadata'))
        detail_serializer = PaymentDetailSerializer(payment, context={'request': request})
        return Response({'detail': 'مبلغ با موفقیت برگشت داده شد.', 'payment': detail_serializer.data})

