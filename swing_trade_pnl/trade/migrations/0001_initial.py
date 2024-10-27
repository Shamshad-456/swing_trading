# Generated by Django 5.1.1 on 2024-10-05 13:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scrip', models.CharField(max_length=100)),
                ('trade_date', models.DateField()),
                ('buy_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
                ('margin', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('interest_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('exchange', models.CharField(blank=True, max_length=50, null=True)),
                ('current_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('pnl', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('interest_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_charges', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('is_open', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]