from rest_framework import serializers
from .models import Song, LyricVersion


class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = "__all__"


class LyricVersionSerializer(serializers.ModelSerializer):

    class Meta:
        model = LyricVersion
        fields = "__all__"