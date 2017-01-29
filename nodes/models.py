from django.db import models


class CollisionNode(models.Model):
    identificador = models.IntegerField(
        verbose_name='Identificador',
        unique=True,
        blank=False,
        null=False
    )

    collisions = models.ManyToManyField(
        to='self',
        verbose_name='Colisões'
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

        bulk = [cls(identificador=key) for key in graph.keys()]
        cls.objects.bulk_create(bulk)

        for key in graph.keys():
            _node = cls.objects.get(key)
            _collisions = cls.objects.filter(
                identificador__in=graph.get(key, [])
            )
            _node.collisions.add(*_collisions)
            _node.save()

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
