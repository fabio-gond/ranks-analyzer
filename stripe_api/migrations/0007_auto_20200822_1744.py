# Generated by Django 2.2 on 2020-08-22 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_api', '0006_plan_days_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
                ('code', models.CharField(blank=True, max_length=32, null=True)),
                ('kwds_qty', models.IntegerField()),
                ('days_step', models.SmallIntegerField(default=3)),
                ('days_duration', models.SmallIntegerField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('stripe_product_id', models.CharField(blank=True, max_length=64, null=True)),
                ('stripe_price_id', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
                ('code', models.CharField(blank=True, max_length=32, null=True)),
                ('kwds_qty', models.IntegerField()),
                ('days_step', models.SmallIntegerField(default=3)),
                ('days_duration', models.SmallIntegerField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('stripe_product_id', models.CharField(blank=True, max_length=64, null=True)),
                ('stripe_price_id', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='plan',
            name='days_duration',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='is_recurring',
        ),
    ]
