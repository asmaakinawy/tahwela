from rest_framework import serializers


class Base_RESPONSE_OBJECT(object):
    def __init__(self, TYPE, TXNSTATUS, TRID, MESSAGE, TXNID):
        self.TYPE       = TYPE
        self.TXNSTATUS  = TXNSTATUS
        self.TRID       = TRID
        self.MESSAGE    = MESSAGE
        self.TXNID      = TXNID

class Base_RESPONSE_SERIALIZER(serializers.Serializer):
    TYPE = serializers.CharField(required=True, allow_blank=False, max_length=100)
    TXNSTATUS = serializers.CharField(required=True, allow_blank=False, max_length=100)
    TXNID = serializers.CharField(required=True, allow_blank=True, max_length=100)
    TRID = serializers.CharField(required=True, allow_blank=True, max_length=100)
    MESSAGE = serializers.CharField(required=True, allow_blank=True)
