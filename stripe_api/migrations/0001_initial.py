# Generated by Django 2.2 on 2020-08-19 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_recurring', models.BooleanField(default=False)),
                ('stripe_plan_id', models.CharField(blank=True, max_length=64, null=True)),
                ('stripe_product_id', models.CharField(blank=True, max_length=64, null=True)),
                ('stripe_price_id', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
    ]