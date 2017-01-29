from rest_framework import viewsets

from nodes.models import CollisionNode
from nodes.serializers import CollisionNodeSerializer


class NodeViewSet(viewsets.ModelViewSet):
    queryset = CollisionNode.objects.all()
    serializer_class = CollisionNodeSerializer
    lookup_field = 'identificador'
