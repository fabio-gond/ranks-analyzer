# Generated by Django 2.2 on 2020-08-10 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0006_keyword'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyword',
            name='productParent',
        ),
    ]
