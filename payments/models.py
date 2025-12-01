from django.db import models
from django.utils import timezone
from reservations.models import Reservation


class Payment(models.Model):
    class Gateway(models.TextChoices):
        ZARINPAL = 'ZARINPAL', 'زرین‌پال'
        MELLAT = 'MELLAT', 'بانک ملت'
        SANDBOX = 'SANDBOX', 'درگاه تستی'

    class Status(models.TextChoices):
        INITIATED = 'INITIATED', 'در انتظار پرداخت'
        PROCESSING = 'PROCESSING', 'در حال پردازش'
        SUCCESS = 'SUCCESS', 'موفق'
        FAILED = 'FAILED', 'ناموفق'
        REFUNDED = 'REFUNDED', 'برگشت داده شده'

    reservation = models.ForeignKey(
        Reservation,
        related_name='payments',
        on_delete=models.CASCADE,
        verbose_name="رزرو",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="مبلغ")
    gateway = models.CharField(
        max_length=20,
        choices=Gateway.choices,
        default=Gateway.SANDBOX,
        verbose_name="درگاه",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.INITIATED,
        verbose_name="وضعیت",
    )
    authority = models.CharField(max_length=64, unique=True, verbose_name="کد رهگیری")
    reference_id = models.CharField(max_length=64, null=True, blank=True, verbose_name="کد مرجع")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان پرداخت")
    metadata = models.JSONField(default=dict, blank=True, verbose_name="اطلاعات تکمیلی")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reservation', 'status']),
            models.Index(fields=['authority']),
        ]

    def __str__(self):
        return f"Payment {self.authority} - {self.get_status_display()}"

    @staticmethod
    def generate_authority():
        import uuid

        return uuid.uuid4().hex[:16].upper()

    def mark_processing(self):
        self.status = self.Status.PROCESSING
        self.save(update_fields=['status', 'updated_at'])

    def mark_success(self, reference_id=None, metadata=None):
        self.status = self.Status.SUCCESS
        self.reference_id = reference_id or self.reference_id
        self.paid_at = timezone.now()
        if metadata:
            current = self.metadata or {}
            current.update(metadata)
            self.metadata = current
        self.save(update_fields=['status', 'reference_id', 'paid_at', 'metadata', 'updated_at'])
        self.reservation.mark_as_paid()

    def mark_failed(self, metadata=None):
        self.status = self.Status.FAILED
        if metadata:
            current = self.metadata or {}
            current.update(metadata)
            self.metadata = current
        self.save(update_fields=['status', 'metadata', 'updated_at'])
        self.reservation.mark_as_failed()

    def mark_refunded(self, metadata=None):
        self.status = self.Status.REFUNDED
        if metadata:
            current = self.metadata or {}
            current.update(metadata)
            self.metadata = current
        self.save(update_fields=['status', 'metadata', 'updated_at'])
        self.reservation.mark_as_refunded()
