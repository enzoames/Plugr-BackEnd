# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *

# Create your views here.

class PhotologueViewset(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class PhotoByGalleryViewSet(viewsets.ModelViewSet):
	serializer_class = EnzoGallerySerializer

	def get_queryset(self):
		queryset = { 'result': 'none' }

		if self.kwargs['slug']:
			queryParam = self.kwargs['slug']
			
			if str(queryParam) == 'covers':
				queryset = EnzoGallery.objects.filter(photo_description='gallery_cover')
			elif str(queryParam) == 'vertical':
				queryset = EnzoGallery.objects.filter(orientation='vertical')
			else:
				queryset = EnzoGallery.objects.filter(gallery_name=queryParam)
		
		return queryset



class ContactEnzoAmesViewSet(viewsets.ModelViewSet):
	queryset = ContactEnzoAmes.objects.all()
	serializer_class = ContactEnzoAmesSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)

	def create(self, request, format=None):
		print ("\nREQUEST:::\n")
		print (request)
		print (request.data)

		firstname = request.data.get('firstname', None) 
		lastname = request.data.get('lastname', None)
		company = request.data.get('company', None)
		email = request.data.get('email', None)
		message = request.data.get('message', None)

		registerdata = {
			'firstname': firstname,
			'lastname': lastname,
			'company': company,
			'email': email,
			'message': message
		}

		serializer = ContactEnzoAmesSerializer(data=registerdata)

		if serializer.is_valid():
		 	contact_information = serializer.create(serializer.validated_data) #passing register data again. This is a work around
			return Response(status=status.HTTP_201_CREATED)
		else:
			print("\n ==============")
			print(serializer.errors)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




