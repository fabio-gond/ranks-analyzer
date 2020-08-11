# Generated by Django 2.2 on 2020-08-10 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.CharField(max_length=512)),
                ('context', models.CharField(max_length=32)),
                ('severity', models.SmallIntegerField()),
                ('time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]