from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    publishing_datetime = models.DateTimeField()
    thumbnail_url = models.URLField()
    video_id = models.CharField(max_length=100, default=0, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['publishing_datetime']),
        ]

    def __str__(self):
        return self.title