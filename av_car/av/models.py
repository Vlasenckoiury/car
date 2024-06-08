from django.db import models
from django.utils.translation import gettext as _


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

class BotUser(models.Model):
    telegram_id = models.PositiveBigIntegerField(_('ID Telegram'), db_index=True, unique=True)
    username = models.CharField(_('Username'), max_length=100, blank=True, null=True)
    first_name = models.CharField(_('Имя'), max_length=100, blank=True, null=True)
    last_name = models.CharField(_('Фамилия'), max_length=100, blank=True, null=True)
    contact = models.CharField(_('Телефон'), max_length=100, blank=True, null=True)

    class Meta:
        app_label = "av_car"
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'

    def __str__(self):
        return f'{self.telegram_id} {self.username}'


class TelegramChat(models.Model):
    name = models.CharField(_('Имя канала'),
                            max_length=150, blank=True, null=True, help_text='Имя Канала')
    chat_link = models.CharField(_('Ссылка канала'),
                                 max_length=150, db_index=True, help_text='Пример ссылки: https://t.me/test')

    def __str__(self):
        return f'{self.chat_link} {self.name}'

    class Meta:
        verbose_name = 'Телеграм канал'
        verbose_name_plural = 'Телеграм каналы'


class InviteLink(models.Model):
    # Пригласительные ссылки
    telegram_chat = models.ForeignKey(TelegramChat, verbose_name=_('Телеграм канал'), on_delete=models.CASCADE)
    creates_join_request = models.BooleanField(_('Запрос на добавление'), default=True)
    creator = models.CharField(_('Создатель'), max_length=250, blank=True, null=True)
    expire_date = models.CharField(_('expire_date'), max_length=150, blank=True, null=True)
    link = models.CharField(_('Ссылка'), max_length=150, blank=True, null=True)
    is_primary = models.BooleanField(_('Is_primary'), blank=True, null=True)
    is_revoked = models.BooleanField(_('Is_revoked'), blank=True, null=True)
    member_limit = models.IntegerField(_('Лимит подписок'), blank=True, null=True)
    name = models.CharField(_('name'), max_length=150, blank=True, null=True)
    pending_join_request_count = models.IntegerField(_('pending_join_request_count'), blank=True, null=True)

    def __str__(self):
        return f'{self.link}'

    class Meta:
        verbose_name = 'Пригласительная ссылка'
        verbose_name_plural = 'Пригласительные ссылки'


class TelegramSubscriber(models.Model):
    invite_link = models.ForeignKey(TelegramChat, verbose_name=_('Канал'), on_delete=models.CASCADE)
    telegram_id = models.PositiveBigIntegerField(_('ID Telegram'), db_index=True, unique=True)
    username = models.CharField(_('Username'), max_length=100, blank=True, null=True)
    first_name = models.CharField(_('Имя'), max_length=100, blank=True, null=True)
    last_name = models.CharField(_('Фамилия'), max_length=100, blank=True, null=True)
    subcribed = models.BooleanField(_('Подписан'), default=False)
    datetime_subscribe = models.DateTimeField(_('Время подписки'), blank=True, null=True)
    datetime_unsubscribe = models.DateTimeField(_('Время отписки'), blank=True, null=True)

    def __str__(self):
        return f'{self.telegram_id}: {self.username}'

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'


class NewMessage(models.Model):
    link_chat = models.ForeignKey(TelegramChat, on_delete=models.CASCADE, verbose_name=_('Канал'), related_name='messages')
    message = models.TextField((_('Новость')))
    start_time = models.TimeField(_('Время начало'), default=None, blank=True, null=False, help_text='Пример ввода времени: 10:00:00')
    end_time = models.TimeField(_('Время конца'), default=None, blank=True, null=False, help_text='Пример ввода времени: 10:00:00')
    created_at = models.DateTimeField(_('Время добавления новости'), blank=True, null=True, auto_now_add=True)
    day_monday = models.BooleanField(_('Понедельник'), default=False)
    day_tuesday = models.BooleanField(_('Вторник'), default=False)
    day_wednesday = models.BooleanField(_('Среда'), default=False)
    day_thursday = models.BooleanField(_('Четверг'), default=False)
    day_friday = models.BooleanField(_('Пятница'), default=False)
    day_saturday = models.BooleanField(_('Суббота'), default=False)
    day_sunday = models.BooleanField(_('Воскресенье'), default=False)

    def boolean_to_int(self):
        days = {
            self.day_monday: 0,
            self.day_tuesday: 1,
            self.day_wednesday: 2,
            self.day_thursday: 3,
            self.day_friday: 4,
            self.day_saturday: 5,
            self.day_sunday: 6
        }
        res = [value for day, value in days.items() if day]
        if res:
            return res[0]
        else:
            return res

    def __str__(self):
        return f'{self.message}'

    class Meta:
        verbose_name = 'Новости и расписание канала'
        verbose_name_plural = 'Новости и расписание каналов'


class AskMessage(models.Model):
    chat_id = models.BigIntegerField(_('Чат Id'), default=False, blank=True, null=True)
    question = models.TextField(_('Вопрос'), default=None, blank=True, null=True)
    answer = models.TextField(_('Ответ'), default=False, blank=True, null=True)
    result = models.BooleanField(_('Результат'), default=False, help_text='Отметьте если ответили на вопрос', blank=True, null=True)
    created_at = models.DateTimeField(_('Время добавления'), blank=True, null=True, auto_now_add=True)

    def __str__(self):
        return f'{self.question}'

    class Meta:
        verbose_name = 'Вопрос и Ответ'
        verbose_name_plural = 'Вопросы и Ответы'
