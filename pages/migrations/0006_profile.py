# Generated by Django 5.2.1 on 2025-05-16 15:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_alter_posttag_icon'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('personal_story', models.TextField(blank=True)),
                ('post_count', models.PositiveIntegerField(default=0)),
                ('hugs_count', models.PositiveIntegerField(default=0)),
                ('connections_count', models.PositiveIntegerField(default=0)),
                ('interests', models.ManyToManyField(blank=True, to='pages.posttag')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
