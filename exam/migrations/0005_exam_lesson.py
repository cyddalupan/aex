# Generated by Django 5.0.2 on 2024-03-13 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exam", "0004_alter_exam_audio_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="exam",
            name="lesson",
            field=models.CharField(blank=True, max_length=510, null=True),
        ),
    ]