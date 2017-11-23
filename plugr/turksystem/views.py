# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from django.shortcuts import render, HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *

from django.forms.models import model_to_dict


# Create your views here.

# ========================================================================================================================
# ========================================================================================================================
# ================================================ ENZO ==================================================================
# ========================================================================================================================
# ========================================================================================================================


class TurkUserViewSet(viewsets.ModelViewSet):
    serializer_class = TurkUserSerializer

    def get_queryset(self):
        queryset = { 'result': 'none' }

        if self.kwargs:
            url_param = self.kwargs['slug']
            if str(url_param) == 'developer':
                queryset = TurkUser.objects.filter(credential='developer')
            elif str(url_param) == 'client':
                queryset = TurkUser.objects.filter(credential='client')
            else:
                queryset = TurkUser.objects.filter(id=url_param)
        else:
            queryset = TurkUser.objects.all()

        return queryset


class LoadTurkUserViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    queryset = TurkUser.objects.all()
    serializer_class = TurkUserSerializer


class LoginTurkUserViewSet(viewsets.ModelViewSet):

    def create(self, request, format=None):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if TurkUser.objects.filter(email=email, password=password).exists():
            requested_user = TurkUser.objects.get(email=email, password=password)
            returned_user = model_to_dict(requested_user)
            del returned_user['password']
            returned_dict = {
                'user': returned_user
            }
            return Response(returned_dict, status=status.HTTP_202_ACCEPTED)
        else:
            requested_user = {'error': 'invalid credentials'}
            return Response(requested_user, status=status.HTTP_404_NOT_FOUND)


class LogoutTurkUserViewSet(viewsets.ModelViewSet):
    def create(self, request, format=None):
        response_dict = {'logout': 'succesfully'}
        return Response(response_dict, status=status.HTTP_202_ACCEPTED)


class RegisterViewSet(viewsets.ModelViewSet):
    def create(self, request, format=None):
        print("\nREQUEST:::\n")
        print(request)
        print(request.data)
        TurkUsers = TurkUser.objects.all()
        name = request.data.get('firstname', None)
        lastname = request.data.get('lastname', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        registerdata = {
            'name': name,
            'lastname': lastname,
            'email': email,
            'password': password
        }

        if TurkUsers.filter(email=email).exists():
            response = {'error': 'There already exists a user associated with this email'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            if BlackList.objects.filter(user__email=email).exists():
                reason = BlackList.objects.get(user__email=email).reason
                response = {'error': reason}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = RegisterSerializer(data=registerdata)
                if serializer.is_valid():

                    register_information = serializer.create(serializer.validated_data)
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    print(serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BidBySDIDViewSet(viewsets.ModelViewSet): # given the id of a System Demand, returns all bids associated to it
    serializer_class = BidSerializer
    def get_queryset(self):
        if self.kwargs:
            bid_sd = self.kwargs['sd']
            queryset = Bid.objects.filter(systemdemand__id=bid_sd)
        return queryset

class BidByEmailViewSet(viewsets.ModelViewSet): # given a email, returns all bids for that email.
    serializer_class = BidSerializer
    def get_queryset(self):
        query_param = self.request.query_params.get('email', None)
        if query_param:
            user = TurkUser.objects.get(email=str(query_param))
            if user.credential == 'developer':
                print ("developer")
                queryset = Bid.objects.filter(developer__email=user.email)
            elif user.credential == 'client':
                print ("client")
                queryset = Bid.objects.filter(systemdemand__client__email=user.email)        
        return queryset


# ========================================================================================================================
# ========================================================================================================================
# ================================================ ROHAN =================================================================
# ========================================================================================================================
# ========================================================================================================================


class SysDemandViewSet(viewsets.ModelViewSet):    
    serializer_class = SysDemandSerializer

    def get_queryset(self):
        if self.kwargs:
            url_param = self.kwargs['pk']
            queryset = SystemDemand.objects.filter(id=url_param)
        else:
            queryset = SystemDemand.objects.all()
        return queryset

    def create(self, request, format=None):
        title = request.data.get('title')
        precondition = request.data.get('precondition')
        postcondition = request.data.get('postcondition')
        description = request.data.get('description')
        deadline = request.data.get('deadline')
        reward = request.data.get('reward')
        client = request.data.get('client')
        Sysstatus = request.data.get('status')

        if TurkUser.objects.filter(email = client).exists():
            client = TurkUser.objects.get(email=client)
            json_client = model_to_dict(client)
            
            sysDemandData = {
                'title': title,
                'precondition': precondition,
                'postcondition': postcondition,
                'description': description,
                'deadline': deadline,
                'reward': reward,
                'client': client,
                'status': Sysstatus
            }

            SystemDemand.objects.create(**sysDemandData)#reminder to Rohan to fix
            sysDemandData["client"] = json_client
            return Response(sysDemandData,status=status.HTTP_201_CREATED)
        else:
            error = { 'error': 'Client Not found'}
            return Response(error, status=status.HTTP_404_NOT_FOUND)


class BidViewSet(viewsets.ModelViewSet):
    serializer_class = BidSerializer
    queryset = Bid.objects.all() # all bids

    def create(self, request, format=None):
        price = request.data.get("price")
        developer = request.data.get("developer")
        systemdemand = request.data.get("systemdemand")

        if (TurkUser.objects.filter(email = developer).exists() and
            SystemDemand.objects.filter(id = systemdemand).exists()):

            postbid ={
                "price":price,
                "developer":TurkUser.objects.get(email=developer),
                "systemdemand":SystemDemand.objects.get(id=systemdemand)
                }

            Bid.objects.create(**postbid)
            return Response(status=status.HTTP_201_CREATED)
        else:
            error = { 'error': 'Client Not found'}
            return Response(error,status=status.HTTP_404_NOT_FOUND)


