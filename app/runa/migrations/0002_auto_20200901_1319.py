# Generated by Django 3.0.7 on 2020-09-01 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set(),
        ),
    ]
