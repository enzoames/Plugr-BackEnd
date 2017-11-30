# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import F
from rest_framework import viewsets
from django.shortcuts import render, HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
import json
from django.core import serializers
from django.forms.models import model_to_dict


# from django.http import JsonResponse might be helpful
# Create your views here.

# ========================================================================================================================
# ========================================================================================================================
# ================================================ ENZO ==================================================================
# ========================================================================================================================
# ========================================================================================================================
class TurkUserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = TurkUserSerializer
    queryset = TurkUser.objects.all()

    def put(self, request):
        user_id = request.data.get('user_id', None)
        resume = request.data.get('resume', None)
        technical_skills = request.data.get('technical_skills', None)
        project_experience = request.data.get('project_experience', None)
        interests = request.data.get('interests', None)
        recent_work = request.data.get('recent_work', None)
        business_credential = request.data.get('business_credential', None)

        turkuser = TurkUser.objects.get(id=user_id)
        data = {
            'user_id': user_id,
            'resume': resume,
            'technical_skills': technical_skills,
            'project_experience': project_experience,
            'interests': interests,
            'recent_work': recent_work,
            'business_credential': business_credential
        }

        # USEFUL!
        # final_data = dict(map(lambda item: (item[0], item[1]), data.items()))
        # print (final_data)
        final_data = dict(filter(lambda item: item[1] != "", data.items()))

        serializer = TurkUserSerializer(data=final_data)
        if serializer.is_valid():
            updated_information = serializer.update(serializer.validated_data, turkuser)
            return Response(model_to_dict(updated_information), status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TurkUserViewSet(viewsets.ModelViewSet):
    serializer_class = TurkUserSerializer

    def get_queryset(self):
        queryset = {'result': 'none'}
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
        credential = request.data.get('credential', None)

        registerdata = {
            'name': name,
            'lastname': lastname,
            'email': email,
            'password': password,
            'credential': credential
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
                    return Response(model_to_dict(register_information), status=status.HTTP_201_CREATED)
                else:
                    print(serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BidBySDIDViewSet(viewsets.ModelViewSet):  # given the id of a System Demand, returns all bids associated to it
    serializer_class = BidSerializer

    def get_queryset(self):
        if self.kwargs:
            bid_sd = self.kwargs['sd']
            queryset = Bid.objects.filter(systemdemand__id=bid_sd)
        return queryset


class BidByEmailViewSet(viewsets.ModelViewSet):  # given a email, returns all bids for that email.
    serializer_class = BidSerializer

    def get_queryset(self):
        queryset = {'bid': 'none'}
        query_param = self.request.query_params.get('email', None)
        if query_param:
            user = TurkUser.objects.get(email=str(query_param))
            if user.credential == 'developer':
                print("developer")
                queryset = Bid.objects.filter(developer__email=user.email)
            elif user.credential == 'client':
                print("client")
                queryset = Bid.objects.filter(systemdemand__client__email=user.email)
                # client_bids = Bid.objects.filter(systemdemand__client__email=user.email)
                # client_bids = json.dumps(list(client_bids.values()), indent=4, sort_keys=True, default=str)
                # client_SDs = SystemDemand.objects.filter(client__email=user.email)
                # client_SDs = json.dumps(list(client_SDs.values()), indent=4, sort_keys=True, default=str)
        return queryset


class SysDemandByClientViewSet(viewsets.ModelViewSet):  # passing query parameter to get all SDs from a single client
    serializer_class = SysDemandSerializer

    def get_queryset(self):
        query_param = self.request.query_params.get('email', None)
        if query_param:
            queryset = SystemDemand.objects.filter(client__email=str(query_param))
        else:
            queryset = SystemDemand.objects.all()
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

        if TurkUser.objects.filter(email=client).exists():
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

            SystemDemand.objects.create(**sysDemandData)  # reminder to Rohan to fix
            sysDemandData["client"] = json_client
            return Response(sysDemandData, status=status.HTTP_201_CREATED)
        else:
            error = {'error': 'Client Not found'}
            return Response(error, status=status.HTTP_404_NOT_FOUND)


class BidViewSet(viewsets.ModelViewSet):
    serializer_class = BidSerializer
    queryset = Bid.objects.all()  # all bids

    def create(self, request, format=None):
        price = request.data.get('bid')
        dev_email = request.data.get('email')
        sd_id = request.data.get('sdID')

        if not Bid.objects.filter(developer__email=dev_email).filter(systemdemand__id=sd_id).exists():
            data = {
                'price': price,
                'developer': TurkUser.objects.get(email=dev_email),
                # model_to_dict(TurkUser.objects.get(email=dev_email)),
                'systemdemand': SystemDemand.objects.get(id=sd_id)  # model_to_dict(sd)
            }

            Bid.objects.create(**data)
            return Response(status=status.HTTP_201_CREATED)
            # serializer = BidSerializer(data=data)
            # if serializer.is_valid():
            #     print (" === VALID BID POST")
            #     bid_information = serializer.create(serializer.validated_data)
            #     return Response(model_to_dict(bid_information), status=status.HTTP_201_CREATED)
            # else:
            #     print (" === INVALID BID POST")
            #     print(serializer.errors)
            #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            error = {'error': 'There is already a bid in your account for this System Demand'}
            return Response(error, status=status.HTTP_404_NOT_FOUND)


class DepositViewSet(viewsets.ModelViewSet):
    """View set for deposite"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    queryset = TurkUser.objects.all()
    serializer_class = TurkUserSerializer

    def create(self, request, format=None):
        amount = request.data.get("amount")
        user = request.data.get("user")

        if int(amount) < 0:
            error = {'error': 'Cannot deposit negative amount'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        else:
            if TurkUser.objects.filter(email=user).exists():

                TurkUser.objects.filter(email=user).update(money=F("money") + amount)
                return_user = model_to_dict(TurkUser.objects.get(email=user))
                return Response(return_user, status=status.HTTP_202_ACCEPTED)
            else:
                error = {'error': 'Cannot deposit negative amount'}
                Response(error, status=status.HTTP_404_NOT_FOUND)


class TransactionViewSet(viewsets.ModelViewSet):
    """This handles money"""

    def put(self, request, format=None):
        sysdemand = request.data.get("systemdemand")
        client = request.data.get("client")
        developer = request.data.get("developer")

        if (TurkUser.objects.filter(email=client).exists() and
                TurkUser.objects.filter(email=developer).exists() and
                SystemDemand.objects.filter(id=sysdemand).exists()
            ):
            # get sysdemand
            sys = SystemDemand.objects.get(id=sysdemand)
            front_pay = sys.reward / 2

            # subtract money from client
            TurkUser.objects.filter(email=client).update(money=F("money") - front_pay)

            # add money to devepler account
            TurkUser.objects.filter(email=developer).update(money=F("money") + front_pay)
            # i also think we should add the front_pay to the choosen developer table

            dev = model_to_dict(TurkUser.objects.get(email=developer))
            cli = model_to_dict(TurkUser.objects.get(email=client))

            # just for show
            return_dic = {
                "front_Fee": front_pay,
                "client_": cli,
                "developer_": dev
            }

            return Response(return_dic, status=status.HTTP_202_ACCEPTED)
        else:
            Response(status=status.HTTP_400_BAD_REQUEST)
