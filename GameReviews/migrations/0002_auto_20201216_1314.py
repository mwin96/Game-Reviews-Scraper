# Generated by Django 3.1.4 on 2020-12-16 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='link',
            field=models.CharField(default='', max_length=2083),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='releaseDate',
            field=models.DateField(max_length=200),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='score',
            field=models.FloatField(max_length=200),
        ),
    ]