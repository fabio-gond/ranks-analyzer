# Generated by Django 2.2 on 2020-08-19 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customuser_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='paid_until',
            field=models.DateField(null=True),
        ),
    ]