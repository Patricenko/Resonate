# Generated by Django 5.2.4 on 2025-07-12 14:04

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
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('liked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_likes', to=settings.AUTH_USER_MODEL)),
                ('liker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='given_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('liker', 'liked')},
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_as_user1', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_as_user2', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user1', 'user2')},
            },
        ),
        migrations.CreateModel(
            name='Pass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('passed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_passes', to=settings.AUTH_USER_MODEL)),
                ('passer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='given_passes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('passer', 'passed')},
            },
        ),
    ]
