# Generated by Django 5.1.3 on 2025-01-13 15:18

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0002_habit_viewers_alter_entry_date_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(default=datetime.datetime(2025, 1, 13, 15, 18, 1, 682309, tzinfo=datetime.timezone.utc), verbose_name='date of entry'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2025, 1, 13, 15, 18, 1, 681281, tzinfo=datetime.timezone.utc), verbose_name='habit start date'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='title',
            field=models.CharField(default='New Challenge 02LYM', max_length=40),
        ),
        migrations.AlterField(
            model_name='habit',
            name='viewers',
            field=models.ManyToManyField(related_name='shared_habits', to=settings.AUTH_USER_MODEL),
        ),
    ]
