# Generated by Django 3.2 on 2021-05-06 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='description',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='log',
            name='remarks',
            field=models.CharField(default='No Remark', max_length=150),
        ),
    ]
