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


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = get_fields_for_model(BotUser)
    search_fields = ['telegram_id', 'username', 'first_name', 'last_name']
    list_filter = ['telegram_id', 'username', 'first_name', 'last_name']


@admin.register(TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    list_display = get_fields_for_model(TelegramChat)
    list_filter = ['name']


@admin.register(InviteLink)
class InviteLinkAdmin(admin.ModelAdmin):
    list_display = get_fields_for_model(InviteLink)
    list_filter = ['telegram_chat', 'name']


@admin.register(TelegramSubscriber)
class TelegramSubscriberAdmin(admin.ModelAdmin):
    list_display = get_fields_for_model(TelegramSubscriber)
    list_filter = ['telegram_id']


@admin.register(NewMessage)
class NewMessageAdmin(admin.ModelAdmin):
    list_display = get_fields_for_model(NewMessage)
    list_editable = ['message', 'start_time', 'end_time']


@admin.register(AskMessage)
class AskMessage(admin.ModelAdmin):
    list_display = get_fields_for_model(AskMessage)
    list_editable = ['answer']
    list_filter = get_fields_for_model(AskMessage)
