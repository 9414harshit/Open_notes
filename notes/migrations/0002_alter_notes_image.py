# Generated by Django 4.0.6 on 2022-07-17 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='image',
            field=models.ImageField(upload_to='img/'),
        ),
    ]