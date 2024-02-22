# Generated by Django 5.0.2 on 2024-02-22 14:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('family', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='familymember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='family',
            name='members',
            field=models.ManyToManyField(related_name='families', through='family.FamilyMember', to=settings.AUTH_USER_MODEL, verbose_name='Члены семьи'),
        ),
    ]
