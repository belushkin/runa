from django.db import models
from django.conf import settings


class Category(models.Model):

    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    class Meta:
        unique_together = ('name', 'parent',)
        verbose_name_plural = "categories"
        app_label = 'runa'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])
