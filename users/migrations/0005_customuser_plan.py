# Generated by Django 2.2 on 2020-08-19 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_api', '0003_auto_20200819_1146'),
        ('users', '0004_remove_customuser_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stripe_api.Plan'),
        ),
    ]