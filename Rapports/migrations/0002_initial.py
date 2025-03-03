# Generated by Django 5.0.3 on 2025-02-24 17:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Rapports', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='historique',
            name='utilisateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historiques', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rapport',
            name='utilisateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rapports', to=settings.AUTH_USER_MODEL),
        ),
    ]
