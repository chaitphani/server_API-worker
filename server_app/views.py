from time import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from server_app.models import phone_number
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)


class BoundSmsSerializer(serializers.Serializer):

    _to = serializers.CharField(required=True)
    _from = serializers.CharField(required=True)
    _text = serializers.CharField(required=True)  


class InboundApiView(APIView):

    '''
        API to send in bound SMS to the number provided with the validations

    '''

    # this will be used to work from browser flexibility
    serializer_class = BoundSmsSerializer

    # this is to check authentications
    permission_classes = (IsAuthenticated,)

    # method used to post the requested data
    def post(self, request) -> dict:
        
        _to = self.request.data.get('_to')
        _from = self.request.data.get('_from')
        _text = self.request.data.get('_text')

        serializer_data = BoundSmsSerializer(data=request.data)
        
        # to check/get the logged in users data
        account_user = phone_number.objects.filter(account__user=request.user)
        if len(account_user) > 0:
            user = account_user.last()
        
        if not _to:
            return Response({"message": "", 'error':'to is missing'}, status=status.HTTP_404_NOT_FOUND)
        if not _from:
            return Response({"message": "", 'error':'from is missing'}, status=status.HTTP_404_NOT_FOUND)
        if not _text:
            return Response({"message": "", 'error':'text is missing'}, status=status.HTTP_404_NOT_FOUND)             

        # checking the validation of the serializer with the provided data
        if not serializer_data.is_valid():
            return Response({"message": "", 'error':'unknown failure'}, status=status.HTTP_400_BAD_REQUEST)
        
        # checking for the to value with logged in user number
        if not _to == user.number:
            return Response({"message": "", 'error':'to parameter not found'}, status=status.HTTP_403_FORBIDDEN)

        # checking for word `stop` in the given text and adding from and to instance into cache
        if 'STOP' in _text:
            cache_store_to = cache.set('_to', _to, timeout=100)
            cache_store_from = cache.set('_from', _from, timeout=100)
        return Response({'message': 'inbound sms OK', "error": ''}, status=status.HTTP_200_OK)


class OutboundApiView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = BoundSmsSerializer
        
    def post(self, request) -> dict:
        
        # count = 0
        _to = self.request.data.get('_to')
        _from = self.request.data.get('_from')
        _text = self.request.data.get('_text')

        account_user = phone_number.objects.filter(account__user=request.user)
        if len(account_user) > 0:
            user = account_user.last()  

        from_cache = cache.get('_from')
        to_cache = cache.get('_to')

        serializer_data = BoundSmsSerializer(data=request.data)

        if not _to:
            return Response({"message": "", 'error':'to is missing'}, status=status.HTTP_404_NOT_FOUND)
        if not _from:
            return Response({"message": "", 'error':'from is missing'}, status=status.HTTP_404_NOT_FOUND)
        if not _text:
            return Response({"message": "", 'error':'text is missing'}, status=status.HTTP_404_NOT_FOUND) 

        if _from == from_cache and _to == to_cache:
            error_msg = 'sms from {} to {} blocked by STOP request'.format(_from, _to)
            return Response({'message':'', "error":error_msg})          
    
        if not serializer_data.is_valid():
            return Response({"message": "", 'error':'unknown failure'}, status=status.HTTP_400_BAD_REQUEST)

        if not _from == user.number:
            return Response({"message": "", 'error':'from parameter not found'}, status=status.HTTP_403_FORBIDDEN)

        if _from:
            # count += 1
            key_exists = cache.get(_from)
            if key_exists:
                if key_exists > 50:
                    return Response({'message':'', "error":'limit reached for from {_from}'}, status=status.HTTP_200_OK)
                cache.incr(_from)
            else:
                cache.set('_from', _from, timeout=3600*24)

        return Response({'message':'outbound sms OK', "error":''}, status=status.HTTP_200_OK)
