# Generated by Django 2.2 on 2020-08-19 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plans',
            name='days_step',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='plans',
            name='kwds_qty',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plans',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=6),
            preserve_default=False,
        ),
    ]