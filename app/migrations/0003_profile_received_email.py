# Generated by Django 2.0 on 2017-12-24 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_memory'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='received_email',
            field=models.EmailField(default='cholsoo22001@gmail.com', max_length=254),
            preserve_default=False,
        ),
    ]
