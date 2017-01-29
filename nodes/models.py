from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver


class CollisionNode(models.Model):
    identifier = models.IntegerField(
        verbose_name='Identificador',
        unique=True,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'Nó de Colisão'
        verbose_name_plural = 'Nós de Colisões'

    @classmethod
    def load_file(cls, filepath):
        graph = {}
        if filepath:
            with open(filepath, mode='r', encoding='utf-8') as _file:
                for _line in _file:
                    node_1, node_2 = _line.split(' ')
                    node_1_collisions = graph.get(int(node_1), [])
                    node_1_collisions.append(int(node_2))
                    graph.update({int(node_1): set(node_1_collisions)})

        bulk = [cls(identifier=key) for key in graph.keys()]
        cls.objects.bulk_create(bulk)

        for key in graph.keys():
            _bulk_edges = []
            _node = cls.objects.get(identifier=key)
            _to_nodes = graph.get(key, [])
            _collisions = cls.objects.filter(
                identifier__in=_to_nodes
            )
            if _collisions.count() < len(_to_nodes):
                identifiers = _collisions.values_list(
                    'identifier', flat=True
                ).distinct()
                _bulk_additional_nodes = []
                for identifier in _to_nodes:
                    if identifier not in identifiers:
                        _bulk_additional_nodes.append(
                            cls(identifier=identifier)
                        )
                cls.objects.bulk_create(_bulk_additional_nodes)

            for collision in _collisions.iterator():
                _bulk_edges.append(
                    CollisionEdge(from_node=_node, to_node=collision)
                )
            CollisionEdge.objects.bulk_create(_bulk_edges)

    @classmethod
    def is_same_network(cls, node_1, node_2):
        result = node_1.collisions.filter(pk=node_2.pk).exists()
        if not result:
            result = node_1.collisions.filter(
                pk__in=node_2.collisions.all().values_list(
                    'pk', flat=True
                ).distinct()
            ).exists()

        return result

    def add_collision(self, collision_node):
        if not self.collisions.filter(pk=collision_node.pk).exists():
            self.collisions.add(collision_node)


class CollisionEdge(models.Model):
    from_node = models.ForeignKey('CollisionNode', related_name='origins')
    to_node = models.ForeignKey('CollisionNode', related_name='destinies')

    class Meta:
        unique_together = ('from_node', 'to_node')
