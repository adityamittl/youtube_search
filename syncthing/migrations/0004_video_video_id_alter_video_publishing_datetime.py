# Generated by Django 5.0.4 on 2024-04-06 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('syncthing', '0003_alter_video_publishing_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_id',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='video',
            name='publishing_datetime',
            field=models.DateTimeField(),
        ),
    ]
