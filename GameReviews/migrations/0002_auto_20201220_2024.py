# Generated by Django 3.1.4 on 2020-12-21 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='consoles',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='developer',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='link',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='releaseDate',
            field=models.DateField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='steamReview',
            field=models.CharField(default='', max_length=256),
        ),
    ]
