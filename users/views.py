from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token

# Create your views here.

@api_view(['GET', 'POST'])
def register(request):
	if request.method == "POST":
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			user = serializer.save()
			data['response'] = 'User successfully created'
			data['email'] = user.email
			data['username'] = user.username
			token = Token.objects.get(user=user).key
			data['token'] = token
		else:
			data = serializer.errors
		return Response(data)
				
	return Response(data={'Hello':'Hey'})