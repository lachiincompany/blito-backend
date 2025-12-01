from rest_framework import serializers
from payments.models import Payment
from reservations.models import Reservation
from reservations.api.v1.serializers import ReservationDetailSerializer


class PaymentListSerializer(serializers.ModelSerializer):
    reservation_code = serializers.CharField(source='reservation.reservation_code', read_only=True)
    passenger_phone = serializers.CharField(source='reservation.user.user.phone', read_only=True)
    seat_number = serializers.IntegerField(source='reservation.seat.seat_number', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'reservation',
            'reservation_code',
            'passenger_phone',
            'seat_number',
            'amount',
            'gateway',
            'status',
            'authority',
            'reference_id',
            'paid_at',
            'created_at',
        ]
        read_only_fields = ['amount', 'authority', 'reference_id', 'paid_at', 'created_at']


class PaymentDetailSerializer(PaymentListSerializer):
    reservation_details = ReservationDetailSerializer(source='reservation', read_only=True)

    class Meta(PaymentListSerializer.Meta):
        fields = PaymentListSerializer.Meta.fields + ['metadata', 'reservation_details']


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['reservation', 'gateway']

    def validate_reservation(self, value):
        request = self.context['request']
        user = request.user

        if not (user.is_staff or user.is_superuser) and value.user.user != user:
            raise serializers.ValidationError("شما به این رزرو دسترسی ندارید.")

        if value.payment_status == Reservation.PaymentStatus.PAID:
            raise serializers.ValidationError("این رزرو قبلاً پرداخت شده است.")

        return value

    def create(self, validated_data):
        reservation = validated_data['reservation']
        gateway = validated_data.get('gateway', Payment.Gateway.SANDBOX)

        existing = reservation.payments.filter(
            status__in=[Payment.Status.INITIATED, Payment.Status.PROCESSING, Payment.Status.SUCCESS]
        ).first()
        if existing:
            raise serializers.ValidationError("برای این رزرو یک پرداخت فعال یا موفق وجود دارد.")

        # ایجاد پرداخت و بلافاصله موفق کردن آن (بدون درگاه بیرونی)
        payment = Payment.objects.create(
            reservation=reservation,
            amount=reservation.total_price,
            gateway=gateway,
            authority=Payment.generate_authority(),
        )

        # شبیه‌سازی موفقیت پرداخت داخلی
        payment.mark_success(reference_id="INTERNAL-PAYMENT", metadata={"auto": True})

        return payment


class PaymentStatusSerializer(serializers.Serializer):
    reference_id = serializers.CharField(required=False, allow_blank=True)
    success = serializers.BooleanField()
    metadata = serializers.DictField(required=False)


class PaymentRefundSerializer(serializers.Serializer):
    metadata = serializers.DictField(required=False)

