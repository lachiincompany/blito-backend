from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reservations', '0004_reservation_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='مبلغ')),
                ('gateway', models.CharField(choices=[('ZARINPAL', 'زرین‌پال'), ('MELLAT', 'بانک ملت'), ('SANDBOX', 'درگاه تستی')], default='SANDBOX', max_length=20, verbose_name='درگاه')),
                ('status', models.CharField(choices=[('INITIATED', 'در انتظار پرداخت'), ('PROCESSING', 'در حال پردازش'), ('SUCCESS', 'موفق'), ('FAILED', 'ناموفق'), ('REFUNDED', 'برگشت داده شده')], default='INITIATED', max_length=20, verbose_name='وضعیت')),
                ('authority', models.CharField(max_length=64, unique=True, verbose_name='کد رهگیری')),
                ('reference_id', models.CharField(blank=True, max_length=64, null=True, verbose_name='کد مرجع')),
                ('paid_at', models.DateTimeField(blank=True, null=True, verbose_name='زمان پرداخت')),
                ('metadata', models.JSONField(blank=True, default=dict, verbose_name='اطلاعات تکمیلی')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='reservations.reservation', verbose_name='رزرو')),
            ],
            options={
                'verbose_name': 'پرداخت',
                'verbose_name_plural': 'پرداخت‌ها',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['reservation', 'status'], name='payments_pa_reserva_0d100f_idx'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['authority'], name='payments_pa_authori_c0e6e0_idx'),
        ),
    ]

