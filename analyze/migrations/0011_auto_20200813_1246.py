# Generated by Django 2.2 on 2020-08-13 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0010_amazonrank_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amazonrank',
            name='top_seller',
            field=models.CharField(default='', max_length=64),
        ),
    ]
