# Generated by Django 4.2.20 on 2025-05-10 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wordleapp", "0013_collaborative_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="founditem",
            name="resolved",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="lostitem",
            name="resolved",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
