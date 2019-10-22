from rest_framework import serializers
from dataserver.models import WxUser,Item,FarmUser,Question,Order


class WxUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WxUser
        fields = ('user_openid', 'user_address','user_phonenumber','user_nickname')

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id','item_name','owner','category','vedio_address','pic_address',
            'item_description','item_price','item_num_available','item_guarantee','item_benefit','item_period')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('order_num','user_wxuser','order_deliver_address','order_item','order_effect_time','order_is_active','order_price_paid',
            'order_quantity','order_price_origin','order_tree_ip')

class FarmUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmUser
        fields = ('farm_name','farm_address','farm_description','farm_logo_address','farm_phonenumber','farm_contact')

class QuestionSerializer(serializers.ModelSerializer):
    model = Question
    fields = '__all__'
