# Generated by Django 2.2 on 2019-04-16 16:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0002_auto_20190416_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='action',
            name='verb',
            field=models.CharField(max_length=255),
        ),
    ]
