# Generated by Django 2.2.3 on 2019-08-03 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gugudog', '0004_auto_20190802_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='gudogservice',
            name='register_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
