# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 20:00
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import schedule.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleEntry',
            fields=[
                ('name', models.SlugField(help_text=b'unique identifier used in URLs and filenames', primary_key=True, serialize=False)),
                ('action', models.CharField(choices=[(b'logger', b'logger - Log the message "running test {name}/{tid}" at log level INFO.'), (b'mock_acquire', b'mock_acquire - Test an acquisition without using the radio.')], help_text=b'action to be scheduled', max_length=50)),
                ('priority', models.SmallIntegerField(default=10, help_text=b'lower number is higher priority (default=10)')),
                ('start', models.BigIntegerField(blank=True, default=schedule.models.next_schedulable_timefn, help_text=b"absolute time (epoch) to start, or leave blank for 'now'")),
                ('stop', models.BigIntegerField(blank=True, help_text=b"absolute time (epoch) to stop, or leave blank for 'never'", null=True)),
                ('relative_stop', models.BooleanField(default=False, help_text=b'stop should be interpreted as seconds after start')),
                ('interval', models.PositiveIntegerField(blank=True, help_text=b'seconds between events, or leave blank to run once', null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('is_active', models.BooleanField(default=True, help_text=b'deactivate an entry to remove it from the scheduler without removing it from the system')),
                ('next_task_time', models.BigIntegerField(editable=False, null=True)),
                ('next_task_id', models.IntegerField(default=1, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='schedule_entries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
                'db_table': 'schedule',
            },
        ),
    ]
