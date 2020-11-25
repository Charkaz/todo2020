# Generated by Django 3.1.3 on 2020-11-24 09:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('start', '0004_auto_20201121_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='loglogin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('browser', models.CharField(max_length=400, null=True)),
                ('os', models.CharField(max_length=400, null=True)),
                ('device', models.CharField(max_length=400, null=True)),
                ('useri', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]