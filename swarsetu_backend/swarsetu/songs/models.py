from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Song(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    genre = models.CharField(max_length=100, blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="songs"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
class LyricVersion(models.Model):

    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name="versions"
    )

    language = models.CharField(max_length=10)

    lyrics_text = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
class Annotation(models.Model):

    lyric_version = models.ForeignKey(
        LyricVersion,
        on_delete=models.CASCADE,
        related_name="annotations"
    )

    start_index = models.IntegerField()

    end_index = models.IntegerField()

    selected_text = models.TextField()

    note = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    