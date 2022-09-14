from rest_framework import serializers
from .models import Element


class ElementsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'


class UpdateElementSerializer(serializers.ModelSerializer):
    url = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    parentId = serializers.CharField(max_length=200, allow_null=True, allow_blank=True)
    size = serializers.IntegerField(allow_null=True)
    type = serializers.CharField(max_length=6)
    date = serializers.CharField(max_length=26)

    class Meta:
        model = Element
        fields = ['url', 'parentId', 'size', 'type', 'date']
