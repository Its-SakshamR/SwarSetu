from django.contrib.auth import authenticate, get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

User = get_user_model()


@api_view(["POST"])
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "username and password required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "user already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({"token": token.key})


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "invalid credentials"}, status=400)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({"token": token.key})