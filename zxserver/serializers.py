from rest_framework import serializers
from zxserver.models import ZxUser,ZxItem,ZxOrder,ZxPrepay_Order,ZxComments
class ZxUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZxUser
        fields = '__all__'

class ZxItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZxItem
        fields = '__all__'

class ZxOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZxOrder
        fields = '__all__'

class ZxPrepay_OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZxPrepay_Order
        fields = '__all__'


class ZxCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZxComments
        fields = '__all__'
