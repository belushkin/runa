# Generated by Django 3.0.7 on 2020-09-01 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runa', '0002_auto_20200901_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
