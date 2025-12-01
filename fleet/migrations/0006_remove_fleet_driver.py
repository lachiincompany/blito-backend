from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0005_fleet_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fleet',
            name='driver',
        ),
    ]


