# Generated by Django 2.2 on 2020-08-09 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0005_auto_20200714_0154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=64)),
                ('marketplace', models.CharField(max_length=3)),
                ('volume', models.IntegerField(blank=True, null=True)),
                ('importance', models.SmallIntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='analyze.Product')),
                ('productParent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='analyze.ProductParent')),
            ],
        ),
    ]