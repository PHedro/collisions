from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from nodes.models import CollisionNode


class CollisionNodeSubSerializer(ModelSerializer):
    identificador = serializers.IntegerField()

    class Meta:
        model = CollisionNode
        fields = ('identificador',)


class CollisionNodeSerializer(ModelSerializer):
    collisions = CollisionNodeSubSerializer(many=True)
    identificador = serializers.IntegerField(required=True)

    class Meta:
        model = CollisionNode
        fields = ('identificador', 'collisions')
