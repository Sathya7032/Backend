from app.models import *
from rest_framework import serializers

class MemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meme
        fields = ['id', 'user', 'description', 'date', 'images', 'likes']  