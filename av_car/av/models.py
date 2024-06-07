from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        app_label = "av"
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Car(models.Model):
    category = models.ForeignKey(Category, related_name='av', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    price = models.CharField(max_length=50, blank=True, null=True)
    price_usd = models.CharField(max_length=50, blank=True, null=True)
    image = models.TextField(max_length=1000, blank=True, null=True)
    parameter = models.TextField(max_length=500, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    modification = models.TextField(max_length=500, blank=True, null=True)
    all_modification = models.TextField(max_length=500, blank=True, null=True)
    location = models.TextField(max_length=500, blank=True, null=True)
    comment = models.TextField(max_length=1000, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = "av"
        ordering = ('name',)
        index_together = (('id', 'name'),)

    def __str__(self):
        return self.name
