# Generated by Django 5.2 on 2025-04-09 09:20

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Donations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_email', models.EmailField(blank=True, max_length=240, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('donated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('charity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donors', to='charity.charity')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
