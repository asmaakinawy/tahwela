import requests
import json
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.serializers import (CreateUserSerializer, LoginSerializer, ConnectAccountSerializer,
                                  MoneyUploadSerializer, MoneyExchnageSerializer, SendMoneySerializer, BaseSerializer)
from accounts.models import AccountData, BankAccount
from accounts.bank_connection import authorise_bank_account, money_transfer


class CreateUserview(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = AccountData.objects.filter(username=data['MOBILE']).first()
        message = "user already registered"
        status_code = "200"
        if not user:
            user = AccountData.objects.create_user(username=data['MOBILE'], password=data['PASSWORD'], email=data['EMAIL'],
                                        date_of_birth=data['DOB'], address=data['ADDRESS'], gender=data['GENDER'],
                                        idnumber=data['IDNUMBER'])
            message = "user registered successfully"
            status_code = "201"

        data.update({"id": user.id,
                    "message": message,
                     "code": status_code})

        return Response(data)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Something went wrong here so access token is not associated with the user, it will work fine in enhancements.

        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = authenticate(username=data['MOBILE'], password=data['PASSWORD'])

        auth = {
            "client_id" : "RpEFZiplGP5pT0snmRjkm7YrDC30igok5OQzUDNL",
            "client_secret" : "pTwtohQfkdFhI7xlaIXh2sY42n74o8WK0VHNCFB5FsuDtiIRTnKlM18CLjD6CfrQQLtADzYfZFJt6H5eZwoHd15rahPaaGMbrxtrOzj1ULey3oK5EgAdndukyBtzszzk",
            "Content-Type": "application/json"}
        data= {
            "username" : user.username,
            "password" : user.password
        }
        if user:
            response = requests.post('http://localhost:8000/auth/token', headers=auth, data=data)
            token = response.json()["access_token"]
            status_code = "200"
        else:
            token = "Invalid"
            status_code = "400"
        data.update({"token":token,
                     "code" : status_code})

        return Response(data)


class ConnectBankAccount(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ConnectAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = authenticate(username=data['MOBILE'], password=data['PASSWORD'])
        if user:
            is_authorised, reference = authorise_bank_account(data)
            if is_authorised:
                BankAccount.objects.connect_bank_account(username=user, bank_name=data['BANK_NAME'], branch_name=data['BRANCH_NAME'],
                                                         account_number=data['ACCOUNT_NUMBER'], account_holder=data['ACCOUNT_HOLDER'], bank_reference=reference, reference=data.get('REFERENCE'))
                data.update({"bank_reference":reference,
                             "status": "200"})
        else:
            data.update({"status": "401",
                         "message": "incorrect data"})
        return Response(data)

class UploadMoney(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = MoneyUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = authenticate(username=data['MOBILE'], password=data['PASSWORD'])
        if user and user.is_allowed_to_add_balance(data['AMOUNT']):
            is_transfer_done, reference = money_transfer(data['BANK_REFERENCE'], data['AMOUNT'])
            if is_transfer_done:
                balance = user.add_balance(data['AMOUNT'])
                data.update({"status": "200",
                             "reference": reference,
                             "BALANCE" : balance
                             })
        else:
            data.update({"status": "400",
                         "reference": None,
                         "message" : "Something went wrong"
                         })

        return Response(data)


class CheckBalance(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        serializer = BaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = authenticate(username=data['MOBILE'], password=data['PASSWORD'])
        if user:
            data = {
                "balance" : user.balance,
                "status" : "200"
            }
        else:
            data = {
                "balance" : None,
                "status" : "400",
                "message": "something went wrong"
            }

        return Response(data)


class CurrencyExchange(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = MoneyExchnageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        response = requests.get("https://api.exchangeratesapi.io/latest?symbols={}".format(data['CURRENCY']))
        return Response(response.text)


class SendMoney(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SendMoneySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        sender = authenticate(username=data['MOBILE'], password=data['PASSWORD'])
        recipient = AccountData.objects.filter(Q(username=data['RECIPIENT_MOBILE']) | Q(email=data['RECIPIENT_EMAIL'])).first()
        if sender and (sender.balance > data['AMOUNT']) and recipient and recipient.is_allowed_to_add_balance(data['AMOUNT']):
            sender.deducte_balance(data['AMOUNT'])
            recipient.add_balance(data['AMOUNT'])
            data.update({"status" : "200",
                         "message": "transafer done"})

        else:
            data.update({"status" : "400",
                         "message": "something went wrong"})

        return Response(data)


