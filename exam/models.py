from datetime import datetime, timezone
from django.db import models

from course.models import Course

# Create your models here.
class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=255)
    audio_url = models.CharField(blank=True, null=True, max_length=250)
    video_embed = models.CharField(blank=True, null=True, max_length=800)
    answer = models.CharField(max_length=255)
    is_video = models.BooleanField(default=False)
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.now(timezone.utc)
        self.save()

    def __str__(self):
        return self.title