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
import datetime
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
        bio = request.data.get('bio', None)
        technical_skills = request.data.get('technical_skills', None)
        project_experience = request.data.get('project_experience', None)
        interests = request.data.get('interests', None)
        recent_work = request.data.get('recent_work', None)
        business_credential = request.data.get('business_credential', None)

        turkuser = TurkUser.objects.get(id=user_id)
        data = {
            'user_id': user_id,
            'resume': resume,
            'bio': bio,
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

            if BlackList.objects.filter(user__email=email).exists():
                reason = BlackList.objects.get(user__email=email).reason
                requested_user = {'error': reason}
                return Response(requested_user, status=status.HTTP_404_NOT_FOUND)

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
        print(request.data)
        id = request.data.get("id")

        if TurkUser.objects.get(id = id).warning_count >= 2:
            TurkUser.objects.filter(id=id).update(pending = True)
            TurkUser.objects.filter(id=id).update(accepted = False)
            data = {
                "user": TurkUser.objects.get(id=id),
                "reason":"too many warnings"
            }

            BlackList.objects.create(**data)

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


class ChosenSDByEmail(viewsets.ModelViewSet):
    serializer_class = ChosenDeveloperSerializer

    def get_queryset(self):
        query_param_email = self.request.query_params.get('email', None)
        query_param_credential = self.request.query_params.get('credential', None)

        if query_param_credential == 'client':
            queryset = ChosenDeveloper.objects.filter(sysdemand__client__email=str(query_param_email))
            get_all_sysdemand = SystemDemand.objects.filter(client__email=query_param_email)
            print(get_all_sysdemand)
            self._checkSysDemandDate(queryset)
            self._remove_if_still_open(get_all_sysdemand)
            # here we check if now() > deadline:
            # this is where we handle
            # if not, the front money and a fixed penalty will be transferred
            #  from the developer back to the client, and the developer
            # will also receive an automatic rating 1 (worst)

        elif query_param_credential == 'developer':
            queryset = ChosenDeveloper.objects.filter(developer__email=str(query_param_email))
        else:
            queryset = ChosenDeveloper.objects.all()
        return queryset

    def _checkSysDemandDate(self, queryset):
        """this will do some stuff regarding the date of each sys demand that belongs to the client"""
        # /api/turksystem/chosensds/?email=jessica@client.com&credential=client
        penalty = 10
        for chosenDev in queryset:

            if chosenDev.sysdemand.deadline < datetime.date.today() and chosenDev.sysdemand.failed == False:
                # take back front fee from developer and give a rating of 1
                SystemDemand.objects.filter(id=chosenDev.sysdemand.id).update(failed=True)  # project is set to fail
                TurkUser.objects.filter(email=str(chosenDev.developer)).update(
                    money=F('money') - (chosenDev.front_fee + penalty))
                Num_cli_rating = TurkUser.objects.get(email=str(chosenDev.developer)).completed_projects
                ave_cli_rating = TurkUser.objects.get(email=str(chosenDev.developer)).rating
                # incase number of rating is 0
                if Num_cli_rating < 1:
                    Num_cli_rating = 1

                if Num_cli_rating > 1:
                    old_sum = (Num_cli_rating - 1) * ave_cli_rating
                    # find the new average rating  of the developer
                    new_ave = (old_sum + 1) / Num_cli_rating
                else:
                    old_sum = Num_cli_rating * ave_cli_rating
                    # find the new average rating  of the developer
                    new_ave = (old_sum + 1) / Num_cli_rating
                # update new ratingupdate
                TurkUser.objects.filter(email=str(chosenDev.developer)).update(rating=new_ave)

    def _remove_if_still_open(self, get_all_sysdemand):
        """this will remove all sysdemands if not chosen"""

        penalty = 10
        for sysdemands in get_all_sysdemand:
            # if sysdemand is not chosen to be worked on before deadline
            if sysdemands.deadline < datetime.date.today() and sysdemands.status == "Open":
                # charge client
                TurkUser.objects.filter(email=str(sysdemands.client)).update(money=F('money') - penalty)
                # delete sysdemand
                SystemDemand.objects.filter(id=sysdemands.id).delete()
                print("somethind just go deleted")


class MessageSuperUserViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSuperUserSerializer

    def create(self, request, format=None):
        print(request.data)
        sender = request.data.get('user')
        complaint = request.data.get('message')

        # current_user = TurkUser.objects.get(pk=sender)
        # print ("========")
        # print (current_user)
        # current_user = model_to_dict(current_user)

        registerdata = {
            'sender': sender,
            'complaint': complaint,
        }

        serializer = MessageSuperUserSerializer(data=registerdata)
        if serializer.is_valid():
            register_information = serializer.create(serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        print(request.data)

        if TurkUser.objects.filter(email=str(client)).exists():
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
                'status': "Open"
            }

            SystemDemand.objects.create(**sysDemandData)  # reminder to Rohan to fix

            sysDemandData["client"] = json_client
            charge = 10
            TurkUser.objects.filter(email=client).update(money=F("money")-charge)
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


class ChooseDeveloperViewSet(viewsets.ModelViewSet):  # might not be the way we need this
    serializer_class = ChosenDeveloperSerializer

    def create(self, request, format=None):
        print(request.data)
        check = True
        response_dic = dict()

        for obj in request.data:

            sysdemand = obj['sdID']
            dev = obj['devID']
            bidPrice = obj['bidPrice']

            if SystemDemand.objects.filter(id=sysdemand).exists():

                developer = TurkUser.objects.get(id=dev)
                system = SystemDemand.objects.get(id=sysdemand)
                front_fee = bidPrice / 2

                data = {
                    "developer": developer,
                    "sysdemand": system,
                    "front_fee": front_fee

                }

                ChosenDeveloper.objects.create(**data)
                print(system.client)

                # removing reward from client account
                TurkUser.objects.filter(email=str(system.client)).update(money=F("money") - front_fee)
                # pay dev half of the bid price bidPrice
                TurkUser.objects.filter(id=dev).update(money=F("money") + front_fee)
                # change status of the sysdemand to closed
                SystemDemand.objects.filter(id=sysdemand).update(status="Closed")
                # change choosen to true
                Bid.objects.filter(systemdemand__id=sysdemand).update(is_chosen=True)
                # Bid.objects.all(systemdemand__id=SystemDemand).exclude(developer__id=dev).delete()

                Bid.objects.filter(systemdemand__id=sysdemand).exclude(developer__id=dev).delete()

            else:
                check = False
                response_dic[sysdemand] = "this systemdemand does not exist"

        if check:
            return Response(status.HTTP_201_CREATED)
        else:
            return Response(response_dic, status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        result1 = request.data.get('result')
        sysdemand = request.data.get("sdID")
        developer = request.data.get("devID")

        # The updates comes when the developer delivers the systemdemand
        print("Inside update ChooseDeveloperViewSet")
        if (TurkUser.objects.filter(id=developer).exists() and
                SystemDemand.objects.filter(id=sysdemand).exists()
            ):
            # get sysdemand
            # sys = SystemDemand.objects.get(id=sysdemand)
            remaining_balance = ChosenDeveloper.objects.get(sysdemand__id=sysdemand).front_fee
            print(TurkUser.objects.get(credential='superuser'))
            print(remaining_balance)

            # transfer remaining money to the super user account
            TurkUser.objects.filter(credential='superuser').update(money=F('money') + remaining_balance)

            # update date_deliverd, result, is completed and result.
            ChosenDeveloper.objects.filter(sysdemand__id=sysdemand).update(result=result1)  # update result
            ChosenDeveloper.objects.filter(sysdemand__id=sysdemand).update(is_completed=True)  # update is completed
            ChosenDeveloper.objects.filter(sysdemand__id=sysdemand).update(
                delivered_at=datetime.datetime.now())  # update date

            # update  projects completed for clients and developers
            TurkUser.objects.filter(systemdemand__id=sysdemand).update(completed_projects=F('completed_projects') + 1)
            TurkUser.objects.filter(id=developer).update(completed_projects=F('completed_projects') + 1)
            TurkUser.objects.filter(id=developer).update(aveRating_every5Count=F("aveRating_every5Count") + 1)

            contract = model_to_dict(ChosenDeveloper.objects.get(sysdemand__id=sysdemand))

            return Response(contract, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class EvaluateDeliveredSDViewSet(viewsets.ModelViewSet):
    """This viewset is to evaluate the system demand delivered by the developer"""

    def put(self, request, format=None):
        _rating = request.data.get("system_rating", None)
        _note = request.data.get("client_note")  # this will be not when the rating
        sysdemand = request.data.get("sdID")

        if ChosenDeveloper.objects.filter(sysdemand__id=sysdemand).exists():
            message = None
            ChosenDeveloper.objects.filter(sysdemand__id=sysdemand).update(
                client_note=_note)  # need to set this field is black
            ChosenDeveloper.objects.filter(sysdemand__id=sysdemand).update(
                system_rating=_rating)  # update rating on this sysdemand
            developer_for_rating = ChosenDeveloper.objects.get(sysdemand__id=sysdemand).developer
            number_of_rating = TurkUser.objects.get(email=developer_for_rating).completed_projects
            number_of_rating2 = TurkUser.objects.get(email=developer_for_rating).aveRating_every5Count
            # get average rating
            average_rating = TurkUser.objects.get(email=developer_for_rating).rating
            new_ave = None

            if number_of_rating > 1:
                old_sum = (number_of_rating - 1) * average_rating
                # find the new average rating  of the developer
                new_ave = (old_sum + _rating) / number_of_rating

                self.check_every_5_rating(developer_for_rating, _rating, number_of_rating2)
            else:
                old_sum = number_of_rating * average_rating
                # find the new average rating  of the developer
                if number_of_rating == 0:
                    new_ave = 0
                else:
                    new_ave = (old_sum + _rating) / number_of_rating
                # get developer
                self.check_every_5_rating(developer_for_rating, _rating, number_of_rating2)

            # update developer average rating
            TurkUser.objects.filter(email=developer_for_rating).update(rating=new_ave)

            if _rating >= 3:
                remaining_balance = ChosenDeveloper.objects.get(sysdemand__id=sysdemand).front_fee
                # remove money form super user  account and add that to developers account
                superuser_pay = remaining_balance * 0.05
                TurkUser.objects.filter(credential='superuser').update(money=F('money') - (remaining_balance-superuser_pay))
                dev = ChosenDeveloper.objects.get(sysdemand__id=sysdemand).developer
                # add money to developer account

                TurkUser.objects.filter(email=str(dev)).update(money=F('money') + (remaining_balance-superuser_pay))

                message = model_to_dict(TurkUser.objects.get(email=str(dev)))
                # update the system_rating
                del message["password"]
            else:
                message = {'message': 'Rating below 3, dialog between client, develper and admin'}

            return Response(message, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def check_every_5_rating(self, developer, _rating, number_of_rating):
        print(number_of_rating)

        if number_of_rating >= 5:

            print("rating >= 5", TurkUser.objects.get(email=developer).aveRating_every5)

            if TurkUser.objects.get(email=developer).aveRating_every5 <= 2:
                print("warned")
                TurkUser.objects.filter(email=developer).update(warning_count=F("warning_count") + 1)

            TurkUser.objects.filter(email=developer).update(aveRating_every5=0)
            TurkUser.objects.filter(email=developer).update(aveRating_every5Count=0)
            number_of_rating = 1

        average_rating = TurkUser.objects.get(email=developer).aveRating_every5
        # calculate ave rating for 5
        if number_of_rating > 1:
            old_sum = (number_of_rating - 1) * average_rating
            # find the new average rating  of the developer
            new_ave = (old_sum + _rating) / number_of_rating
        else:
            old_sum = number_of_rating * average_rating
            if number_of_rating == 0:
                new_ave = 0
            else:
                new_ave = (old_sum + _rating) / number_of_rating

        # update ave rating

        TurkUser.objects.filter(email=developer).update(aveRating_every5=new_ave)


class RateClientViewSet(viewsets.ModelViewSet):
    serializer_class = ChosenDeveloperSerializer

    def put(self, request, format=None):
        print(request.data)
        rate = request.data.get("client_rating")
        cli = request.data.get("client")
        sysid = request.data.get("sdID")

        if TurkUser.objects.filter(email=cli).exists():
            ChosenDeveloper.objects.filter(sysdemand__id=sysid).update(cli_rating=rate)
            Num_cli_rating = TurkUser.objects.get(email=cli).completed_projects
            ave_cli_rating = TurkUser.objects.get(email=cli).rating
            number_of_rating2 = TurkUser.objects.get(email=cli).aveRating_every5Count
            print("completed ", Num_cli_rating)
            print("aveRating", rate)

            if Num_cli_rating > 1:

                old_sum = (Num_cli_rating - 1) * ave_cli_rating
                # find the new average rating  of the developer
                new_ave = (old_sum + rate) / Num_cli_rating
                self.check_every_5_rating(cli, rate, number_of_rating2)
            else:
                old_sum = Num_cli_rating * ave_cli_rating
                # find the new average rating  of the developer
                new_ave = (old_sum + rate) / Num_cli_rating
                self.check_every_5_rating(cli, rate, number_of_rating2)
            # update new ratingupdate
            print(new_ave)
            TurkUser.objects.filter(email=cli).update(rating=new_ave)
            ChosenDeveloper.objects.filter(sysdemand__client__email=cli).update(finish=True)
            user = model_to_dict(TurkUser.objects.get(email=cli))
            return Response(user, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def check_every_5_rating(self, cli, _rating, number_of_rating):

        if number_of_rating >= 5:

            if TurkUser.objects.get(email=cli).aveRating_every5 <= 2:
                TurkUser.objects.filter(email=cli).update(warning_count=F("warning_count") + 1)
                TurkUser.objects.filter(email=cli).update(warning=True)

            TurkUser.objects.filter(email=cli).update(aveRating_every5=0)
            TurkUser.objects.filter(email=cli).update(aveRating_every5Count=0)

            number_of_rating = 1
        average_rating = TurkUser.objects.get(email=cli).aveRating_every5Count
        # calculate ave rating for 5
        if number_of_rating > 1:
            old_sum = (number_of_rating - 1) * average_rating
            # find the new average rating  of the developer
            new_ave = (old_sum + _rating) / number_of_rating
        else:
            old_sum = number_of_rating * average_rating

            if number_of_rating == 0:
                new_ave = 0
            else:
                new_ave = (old_sum + _rating) / number_of_rating

        # update ave rating

        TurkUser.objects.filter(email=cli).update(aveRating_every5=new_ave)


class DeleteUserViewSet(viewsets.ModelViewSet):
    def create(self, request, format=None):
        # messages to su
        # choosendev
        # bids
        # sysdemands
        # user
        user = request.data.get("id")
        credential = request.data.get("credential")
        print(request.data)

        if credential == "client":
            if SUmessages.objects.filter(sender__id=user).exists():
                SUmessages.objects.filter(sender__id=user).delete()
            if ChosenDeveloper.objects.filter(sysdemand__client__id=user).exists():
                ChosenDeveloper.objects.filter(sysdemand__client__id=user).delete()
            if Bid.objects.filter(systemdemand__client__id=user).exists():
                Bid.objects.filter(systemdemand__client__id=user).delete()
            if SystemDemand.objects.filter(client__id=user).exists():
                SystemDemand.objects.filter(client__id=user).delete()

            TurkUser.objects.filter(id=user).delete()

            print("deleted_client")

        if credential == "developer":
            if SUmessages.objects.filter(sender__id=user).exists():
                SUmessages.objects.filter(sender__id=user).delete()
            if ChosenDeveloper.objects.filter(sysdemand__client__id=user).exists():
                ChosenDeveloper.objects.filter(sysdemand__client__id=user).delete()
            if Bid.objects.filter(systemdemand__client__id=user).exists():
                Bid.objects.filter(systemdemand__client__id=user).delete()

            TurkUser.objects.filter(id=user).delete()

            print("deleted_developer")

        response_dict = {'deleted': 'succesfully'}
        return Response(response_dict, status=status.HTTP_202_ACCEPTED)
