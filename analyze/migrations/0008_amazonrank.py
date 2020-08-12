# Generated by Django 2.2 on 2020-08-11 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0007_remove_keyword_productparent'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmazonRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('indexed', models.BooleanField(default=False)),
                ('amazon_choice', models.BooleanField(default=False)),
                ('rank', models.SmallIntegerField(default=0)),
                ('rank_sponsored', models.SmallIntegerField(default=0)),
                ('page', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('pos_in_age', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('pos_in_page_sponsored', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('top_seller', models.CharField(blank=True, max_length=64, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyze.Keyword')),
            ],
        ),
    ]
