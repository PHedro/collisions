from rest_framework import viewsets

from nodes.models import CollisionNode, CollisionEdge
from nodes.serializers import CollisionNodeSerializer, CollisionEdgeSerializer


class NodeViewSet(viewsets.ModelViewSet):
    queryset = CollisionNode.objects.all()
    serializer_class = CollisionNodeSerializer
    lookup_field = 'identifier'


class EdgeViewSet(viewsets.ModelViewSet):
    queryset = CollisionEdge.objects.all()
    serializer_class = CollisionEdgeSerializer
