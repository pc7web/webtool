from django.shortcuts import HttpResponse
# from rest_framework.response import Response
# from rest_framework.decorators import api_view

# Create your views here.
# @api_view(["GET"])
def home(request):
    return HttpResponse('{"message": "welcome"}')
    # return Response({"message": "welcome"})

