# Generated by Django 2.2 on 2020-07-14 01:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('analyze', '0004_auto_20200714_0045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='seller',
        ),
        migrations.RemoveField(
            model_name='productparent',
            name='seller',
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productparent',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Seller',
        ),
    ]
