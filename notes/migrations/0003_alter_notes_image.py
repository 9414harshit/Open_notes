# Generated by Django 4.0.6 on 2022-07-17 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_alter_notes_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='image',
            field=models.ImageField(blank=True, upload_to='img/'),
        ),
    ]