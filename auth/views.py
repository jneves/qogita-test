from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["POST"])
def login(request, format=None):
    if request.user is None:
        raise Http403

    return Response({"token": Token.objects.create(user=request.user).key})


@api_view(["POST"])
def logout(request, format=None):
    if request.user is None:
        raise Http403

    if "HTTP_AUTHORIZATION" in request.META:
        token_key = request.META["HTTP_AUTHORIZATION"][6:]
    Token.objects.filter(user=request.user, key=token_key).delete()

    return Response({})


@api_view(["POST"])
def logout_all(request, format=None):
    if request.user is None:
        raise Http403

    Token.objects.filter(user=request.user).delete()

    return Response({})
