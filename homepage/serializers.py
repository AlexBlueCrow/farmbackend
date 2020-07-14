from rest_framework import serializers
from .models import AdminUser,VideoFiles,PicFiles,VIMap

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = '__all__'
    

class VideoFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFiles
        fields = '__all__'

class PicFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PicFiles
        fields = '__all__'

class VIMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = VIMap
        fields = '__all__'

