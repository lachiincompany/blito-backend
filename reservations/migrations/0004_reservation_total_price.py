from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_remove_reservation_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='total_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='مبلغ کل'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

