from django.contrib import admin
from django.db.models import ManyToOneRel
from .models import *


# from django.contrib.auth.models import User, Group  # Импорт User, Group


# admin.site.unregister(User)  # удаление Юзер
# admin.site.unregister(Group)  # удаление группы
def get_fields_for_model(db_model):  # функция которая возвращает все поля из модели
    fields = []
    for field in db_model._meta.get_fields():
        if isinstance(field, ManyToOneRel):
            continue
        fields.append(field.name)
    return fields


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price',)
    search_fields = ('id', 'name')
