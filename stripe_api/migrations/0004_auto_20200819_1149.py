# Generated by Django 2.2 on 2020-08-19 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_api', '0003_auto_20200819_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='code',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='name',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]