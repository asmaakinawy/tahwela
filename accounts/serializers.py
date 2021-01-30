from rest_framework import serializers
from accounts.models import AccountData

class BaseSerializer(serializers.Serializer):
    PASSWORD        = serializers.CharField(max_length=30, required=True)
    MOBILE          = serializers.RegexField(regex=r"^([0-9]+)$",required=True, allow_blank=False, max_length=15, min_length=10)

class CreateUserSerializer(BaseSerializer):
    ADDRESS         = serializers.CharField(required=False, allow_blank=True,default="Egypt",allow_null=True)
    IDNUMBER        = serializers.CharField(max_length=30, required=True, allow_blank=False)
    DOB             = serializers.RegexField(regex=r"^[0-9]{4}[19|20][0-9]{2}",required=False, allow_blank=True,allow_null=True)
    GENDER          = serializers.CharField(max_length=30, required=False, allow_blank=True,default="M",allow_null=True)
    EMAIL           = serializers.CharField(max_length=30, required=False, allow_blank=True, allow_null=True)


class LoginSerializer(BaseSerializer):
    EMAIL           = serializers.CharField(max_length=30, required=False, allow_blank=True, allow_null=True)


class ConnectAccountSerializer(BaseSerializer):
    BANK_NAME       = serializers.CharField(max_length=128, required=True)
    BRANCH_NAME     = serializers.CharField(max_length=128, required=True)
    ACCOUNT_NUMBER  = serializers.CharField(max_length=128, required=True)
    ACCOUNT_HOLDER  = serializers.CharField(max_length=128, required=True)
    REFERENCE       = serializers.CharField(max_length=128, required=False)


class MoneyUploadSerializer(BaseSerializer):
    AMOUNT         = serializers.CharField(max_length=128, required=True)
    BANK_REFERENCE      = serializers.CharField(max_length=128, required=True)


class MoneyExchnageSerializer(serializers.Serializer):
    CURRENCY = serializers.CharField(max_length=128, required=True)

class SendMoneySerializer(BaseSerializer):
    AMOUNT                    = serializers.CharField(max_length=128, required=True)
    RECIPIENT_EMAIL           = serializers.CharField(max_length=128, required=False)
    RECIPIENT_MOBILE          = serializers.RegexField(regex=r"^([0-9]+)$",required=False, allow_blank=False, max_length=15, min_length=10)

