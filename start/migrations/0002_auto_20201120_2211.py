# Generated by Django 3.1.3 on 2020-11-20 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activateprofile',
            name='code',
            field=models.IntegerField(blank=True, default=186532, null=True),
        ),
    ]
