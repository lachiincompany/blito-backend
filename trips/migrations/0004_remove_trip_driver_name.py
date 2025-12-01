from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_remove_trip_driver_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='driver_name',
        ),
    ]


