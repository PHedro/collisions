from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from nodes.models import CollisionNode, CollisionEdge


class CollisionNodeSerializer(ModelSerializer):
    identifier = serializers.IntegerField(required=True)

    class Meta:
        model = CollisionNode
        fields = ('identifier',)


class CollisionEdgeSerializer(ModelSerializer):
    from_node_id = serializers.IntegerField(required=True)
    to_node_id = serializers.IntegerField(required=True)

    class Meta:
        model = CollisionEdge
        fields = ('from_node_id', 'to_node_id')
