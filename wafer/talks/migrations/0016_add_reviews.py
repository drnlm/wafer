# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-10 01:26
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import markitup.fields

import wafer.talks.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('talks', '0015_add_withdrawn_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', markitup.fields.MarkupField(
                    blank=True, no_rendered_field=True, null=True,
                    help_text='Comments on the proposal (markdown)')),
                ('_notes_rendered', models.TextField(
                    editable=False, blank=True)),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewAspect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('aspect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talks.ReviewAspect')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='talks.Review')),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='talk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='talks.Talk'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('talk', 'reviewer')]),
        ),
        migrations.AlterUniqueTogether(
            name='score',
            unique_together=set([('review', 'aspect')]),
        ),

        # Catching-up on some other model changes (pretty much noop)
        migrations.AlterField(
            model_name='talk',
            name='authors',
            field=models.ManyToManyField(help_text=wafer.talks.models.authors_help, related_name='talks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='talk',
            name='notes',
            field=models.TextField(blank=True, help_text='Any notes for the conference organisers?  These are not visible to the public.', null=True),
        ),
        migrations.AlterField(
            model_name='talk',
            name='status',
            field=models.CharField(choices=[('A', 'Accepted'), ('R', 'Not Accepted'), ('C', 'Talk Cancelled'), ('U', 'Under Consideration'), ('S', 'Submitted'), ('P', 'Provisionally Accepted'), ('W', 'Talk Withdrawn')], default='S', max_length=1),
        ),
        migrations.AlterField(
            model_name='talk',
            name='talk_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='talks.TalkType'),
        ),
        migrations.AlterField(
            model_name='talktype',
            name='disable_submission',
            field=models.BooleanField(default=False, help_text="Don't allow users to submit talks of this type."),
        ),
        migrations.AlterField(
            model_name='talkurl',
            name='talk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urls', to='talks.Talk'),
        ),
    ]
