from rest_framework import serializers

from dataserver.models import WxUser,Item,FarmUser,Question,Order,Comments,Video,Region,Certification


class WxUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WxUser
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class FarmUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmUser
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Region
        fields = '__all__'

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Certification
        fields='__all__'

class VideoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields='__all__'

class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'