from rest_framework import serializers


class NatProjectShortSerialiser(serializers.Serializer):
    id = serializers.IntegerField()
    title_full = serializers.CharField(max_length=300)
    curator = serializers.CharField(max_length=300)
    responsible = serializers.CharField(max_length=300)
