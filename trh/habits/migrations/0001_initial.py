# Generated by Django 5.1.3 on 2025-01-10 11:50

import datetime
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
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='New Challenge IJPN2', max_length=40)),
                ('description', models.CharField(blank=True, default='', max_length=250)),
                ('start_date', models.DateField(default=datetime.datetime(2025, 1, 10, 11, 50, 5, 462134, tzinfo=datetime.timezone.utc), verbose_name='habit start date')),
                ('is_intensity', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime(2025, 1, 10, 11, 50, 5, 462134, tzinfo=datetime.timezone.utc), verbose_name='date of entry')),
                ('entry_text', models.CharField(blank=True, default='', max_length=400)),
                ('intensity', models.IntegerField(blank=True, default=5)),
                ('color', models.CharField(default='#008000', max_length=400)),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habits.habit')),
            ],
        ),
    ]
