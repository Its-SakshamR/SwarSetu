from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .translator import translate_song_lyrics


# GET songs / CREATE song
@api_view(["GET", "POST"])
def song_list_create(request):

    if request.method == "GET":
        songs = Song.objects.all().values()
        return Response(list(songs))

    if request.method == "POST":
        title = request.data.get("title")

        song = Song.objects.create(
            title=title,
            lyrics=""
        )

        return Response({
            "id": song.id,
            "title": song.title
        })


# GET song / UPDATE song
@api_view(["GET", "PUT"])
def song_detail(request, id):

    try:
        song = Song.objects.get(id=id)
    except Song.DoesNotExist:
        return Response(status=404)

    if request.method == "GET":
        return Response({
            "id": song.id,
            "title": song.title,
            "lyrics": song.lyrics
        })

    if request.method == "PUT":
        song.lyrics = request.data.get("lyrics")
        song.save()

        return Response({"status": "updated"})


# Gemini translation endpoint
@api_view(["POST"])
def translate(request):

    text = request.data.get("text")

    translated = translate_song_lyrics(text)

    return Response({
        "translation": translated
    })