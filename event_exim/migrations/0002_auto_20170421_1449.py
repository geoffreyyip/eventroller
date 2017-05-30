# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-04-21 14:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('event_exim', '0001_initial'),
        ('event_store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsource',
            name='origin_organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_store.Organization'),
        ),
        migrations.AddField(
            model_name='eventdupeguesses',
            name='dupe_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dupe_guess_sources', to='event_store.Event'),
        ),
        migrations.AddField(
            model_name='eventdupeguesses',
            name='source_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dupe_guesses', to='event_store.Event'),
        ),
    ]