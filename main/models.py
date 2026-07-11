from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.html import escape
from django.utils.safestring import mark_safe
import re


SUPPORT_FILE_LIMIT = 5 * 1024 * 1024
ONLINE_TIMEOUT_MINUTES = 2


class Olympiad(models.Model):
    TYPE_CHOICES = [('school', 'Школьник'), ('student', 'Студент')]
    STAGE_CHOICES = [('municipal', 'Муниципальный'), ('regional', 'Региональный'), ('all_russia', 'Всероссийский')]
    FORMAT_CHOICES = [('online', 'Заочно (онлайн)'), ('offline', 'Очно')]
    LISTING_TYPE_CHOICES = [('olympiad', 'Олимпиада'), ('grant', 'Грант')]

    public_number = models.PositiveIntegerField(unique=True, null=True, blank=True, verbose_name='Номер карточки')
    listing_type = models.CharField(max_length=12, choices=LISTING_TYPE_CHOICES, default='olympiad', verbose_name='Тип')
    organizer = models.CharField(max_length=255, blank=True, verbose_name='Организатор')
    title = models.CharField(max_length=255)
    link = models.URLField()
    start_date = models.DateField()
    end_date = models.DateField()
    date_added = models.DateField(auto_now_add=True)
    target_audience = models.CharField(max_length=10, choices=TYPE_CHOICES)
    grade = models.IntegerField(null=True, blank=True)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    region = models.CharField(max_length=100, default="Россия")
    short_description = models.CharField(max_length=320, blank=True, verbose_name='Краткое описание')
    description = models.TextField(blank=True, verbose_name='Подробное описание')
    cover_image = models.ImageField(upload_to='olympiad_covers/', blank=True, verbose_name='Обложка')
    is_approved = models.BooleanField(default=False)

    @property
    def is_active(self):
        from datetime import date
        return self.end_date >= date.today()

    @property
    def public_code(self):
        number = self.public_number if self.public_number is not None else self.pk or 0
        return f'#{number:04d}'

    def save(self, *args, **kwargs):
        if self.public_number is None:
            last = Olympiad.objects.exclude(public_number__isnull=True).order_by('-public_number').first()
            self.public_number = (last.public_number + 1) if last else 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True)
    region = models.CharField(max_length=100, blank=True)
    show_region = models.BooleanField(default=False)
    ip_address = models.CharField(max_length=50, blank=True)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True)
    ban_end_date = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Последний вход")
    last_activity = models.DateTimeField(null=True, blank=True, verbose_name="Последняя активность")
    show_last_login = models.BooleanField(default=False, verbose_name="Показывать время входа")
    show_online_status = models.BooleanField(default=True, verbose_name="Показывать онлайн-статус")
    pd_agreement = models.BooleanField(default=False, verbose_name="Согласие на ПДн")
    cookies_agreement = models.BooleanField(default=False, verbose_name="Согласие на Cookies")
    can_upload_photo = models.BooleanField(default=True, verbose_name="Может менять фото профиля")
    can_change_username = models.BooleanField(default=True, verbose_name="Может менять имя аккаунта")
    can_comment = models.BooleanField(default=True, verbose_name="Может писать комментарии")

    @property
    def last_seen(self):
        return self.last_activity or self.last_login or self.user.last_login

    @property
    def is_online(self):
        return bool(self.last_activity and self.last_activity >= timezone.now() - timedelta(minutes=ONLINE_TIMEOUT_MINUTES))

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False, verbose_name='Удалён администратором')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_deleted_comments')
    deleted_at = models.DateTimeField(null=True, blank=True)
    delete_reason = models.TextField(blank=True)
    show_delete_notice = models.BooleanField(default=True, verbose_name='Показывать окно удаления')

    @property
    def html_text(self):
        text = escape(self.text or '')
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.+?)__', r'<u>\1</u>', text)
        text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
        return mark_safe(text.replace('\n', '<br>'))

    def __str__(self):
        return f'{self.user.username}: {self.text[:40]}'


class BannedWord(models.Model):
    word = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.word


class SiteSetting(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.TextField()

    def __str__(self):
        return self.key


class ThemePreset(models.Model):
    """Редактируемая тема сайта.
    Любую тему можно создать, переименовать, удалить и настроить одним и тем же редактором.
    """

    CARD_STYLE_CHOICES = [
        ('frosted', 'Размытое стекло'),
        ('solid', 'Плотная карточка'),
        ('soft', 'Мягкая светлая'),
        ('outline', 'Контурная'),
        ('metallic', 'Серый металлик'),
        ('dark_glass', 'Тёмное стекло'),
        ('telegram', 'Telegram clean'),
        ('discord', 'Discord panel'),
        ('instagram', 'Instagram soft'),
    ]

    BACKGROUND_SIZE_CHOICES = [
        ('cover', 'Заполнить'),
        ('contain', 'Показать полностью'),
        ('100% auto', 'По ширине'),
        ('auto 100%', 'По высоте'),
        ('auto', 'Оригинальный размер'),
    ]

    BACKGROUND_POSITION_CHOICES = [
        ('center center', 'Центр'),
        ('center top', 'Верх'),
        ('center bottom', 'Низ'),
        ('left center', 'Слева'),
        ('right center', 'Справа'),
    ]

    key = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=80, default='Новая тема')
    is_builtin = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=100)

    font_family = models.CharField(max_length=120, default='Inter', blank=True)
    base_font_size = models.PositiveSmallIntegerField(default=16)
    interface_scale = models.DecimalField(max_digits=3, decimal_places=2, default=1.25)

    background_color = models.CharField(max_length=7, default='#eef6fb')
    background_image = models.ImageField(upload_to='themes/presets/images/', blank=True)
    background_gif = models.ImageField(upload_to='themes/presets/gifs/', blank=True)
    background_size = models.CharField(max_length=20, choices=BACKGROUND_SIZE_CHOICES, default='cover')
    background_position = models.CharField(max_length=20, choices=BACKGROUND_POSITION_CHOICES, default='center center')
    background_opacity = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)
    overlay_effect = models.CharField(max_length=20, default='none', choices=[('none','Нет'),('snow','Снег'),('rain','Дождь'),('custom_gif','GIF поверх сайта')])
    overlay_opacity = models.DecimalField(max_digits=3, decimal_places=2, default=0.35)
    overlay_gif = models.ImageField(upload_to='themes/presets/overlays/', blank=True)

    card_color = models.CharField(max_length=7, default='#ffffff')
    card_transparency = models.DecimalField(max_digits=3, decimal_places=2, default=0.88)
    card_blur = models.PositiveSmallIntegerField(default=18)
    card_style = models.CharField(max_length=20, choices=CARD_STYLE_CHOICES, default='frosted')
    card_border_opacity = models.DecimalField(max_digits=3, decimal_places=2, default=0.24)
    card_shadow_opacity = models.DecimalField(max_digits=3, decimal_places=2, default=0.12)
    reflection_strength = models.DecimalField(max_digits=3, decimal_places=2, default=0.25)

    text_color = models.CharField(max_length=7, default='#17212b')
    text_opacity = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)
    muted_color = models.CharField(max_length=7, default='#657786')
    primary_color = models.CharField(max_length=7, default='#229ED9')
    danger_color = models.CharField(max_length=7, default='#e0245e')

    custom_css = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class CustomTheme(models.Model):
    """
    Единая запись с настройками всех тем сайта и виджета обращений.
    Редактируется из вкладки «Темы» в кастомной админ-панели.
    """

    GIF_SIZE_CHOICES = [
        ('contain', 'Показывать полностью'),
        ('cover', 'Заполнить весь экран'),
        ('100% auto', 'Растянуть по ширине'),
        ('auto 100%', 'Растянуть по высоте'),
    ]

    GIF_POSITION_CHOICES = [
        ('center center', 'По центру'),
        ('center top', 'Сверху по центру'),
        ('center bottom', 'Снизу по центру'),
        ('left center', 'Слева по центру'),
        ('right center', 'Справа по центру'),
    ]

    CARD_STYLE_CHOICES = [
        ('frosted', 'Размытое стекло'),
        ('solid', 'Непрозрачные карточки'),
        ('outline', 'Тонкая рамка без заливки'),
        ('metallic', 'Серый металлик'),
        ('dark_glass', 'Тёмное стекло'),
    ]

    # === Общие настройки ===
    font_family = models.CharField(max_length=120, default="Inter", blank=True, verbose_name="Шрифт всего сайта")
    base_font_size = models.PositiveSmallIntegerField(default=16, verbose_name="Размер шрифта сайта")
    interface_scale = models.CharField(max_length=4, default="1.0", verbose_name="Масштаб версии покрупнее")
    metallic_text = models.BooleanField(default=False, verbose_name="Металлик-серый текст")
    text_outline_enabled = models.BooleanField(default=False, verbose_name="Включить обводку текста")
    text_outline_color = models.CharField(max_length=7, default="#ffffff", verbose_name="Цвет обводки текста")
    text_outline_strength = models.PositiveSmallIntegerField(default=0, verbose_name="Толщина обводки текста")

    # === Голубая белая ===
    telegram_background_color = models.CharField(max_length=7, default="#eef6fb", verbose_name="Фон голубой темы")
    telegram_card_color = models.CharField(max_length=20, default="#ffffff", verbose_name="Карточки голубой темы")
    telegram_card_transparency = models.CharField(max_length=4, default="0.88", verbose_name="Прозрачность карточек голубой темы")
    telegram_card_blur = models.PositiveSmallIntegerField(default=18, verbose_name="Размытие карточек голубой темы")
    telegram_card_style = models.CharField(max_length=20, choices=CARD_STYLE_CHOICES, default='frosted', verbose_name="Стиль карточек голубой темы")
    telegram_text_color = models.CharField(max_length=7, default="#17212b", verbose_name="Текст голубой темы")
    telegram_text_opacity = models.CharField(max_length=4, default="1.0", verbose_name="Прозрачность текста голубой темы")
    telegram_muted_color = models.CharField(max_length=7, default="#657786", verbose_name="Вторичный текст голубой темы")
    telegram_primary_color = models.CharField(max_length=7, default="#229ED9", verbose_name="Акцент голубой темы")
    telegram_background_image = models.ImageField(upload_to='themes/telegram/', blank=True, verbose_name="Фото-фон голубой темы")
    telegram_background_gif = models.ImageField(upload_to='themes/telegram/', blank=True, verbose_name="GIF-фон голубой темы")
    telegram_background_size = models.CharField(max_length=20, choices=GIF_SIZE_CHOICES, default='cover', verbose_name="Размер фона голубой темы")
    telegram_background_position = models.CharField(max_length=20, choices=GIF_POSITION_CHOICES, default='center center', verbose_name="Позиция фона голубой темы")
    telegram_overlay_opacity = models.CharField(max_length=4, default="0.18", verbose_name="Прозрачность пелены голубой темы")

    # === Оригинальная тема ===
    background_color = models.CharField(max_length=7, default="#eef6fb")
    card_color = models.CharField(max_length=20, default="#ffffff")
    text_color = models.CharField(max_length=7, default="#17212b")
    text_opacity = models.CharField(max_length=4, default="1.0", verbose_name="Прозрачность текста оригинальной темы")
    muted_color = models.CharField(max_length=7, default="#657786")
    primary_color = models.CharField(max_length=7, default="#229ED9")
    btn_color = models.CharField(max_length=7, default="#229ED9")
    background_image = models.ImageField(upload_to='themes/', blank=True)
    custom_background_gif = models.ImageField(upload_to='themes/custom/', blank=True, verbose_name="GIF-фон оригинальной темы")
    custom_background_size = models.CharField(max_length=20, choices=GIF_SIZE_CHOICES, default='cover', verbose_name="Размер фона оригинальной темы")
    custom_background_position = models.CharField(max_length=20, choices=GIF_POSITION_CHOICES, default='center center', verbose_name="Позиция фона оригинальной темы")
    custom_overlay_opacity = models.CharField(max_length=4, default="0.18", verbose_name="Прозрачность пелены оригинальной темы")
    custom_css = models.TextField(blank=True, help_text="Дополнительный CSS для оригинальной темы")
    card_transparency = models.CharField(max_length=4, default="1.0", verbose_name="Прозрачность карточек (оригинальная)")
    custom_card_blur = models.PositiveSmallIntegerField(default=18, verbose_name="Размытие карточек оригинальной темы")
    custom_card_style = models.CharField(max_length=20, choices=CARD_STYLE_CHOICES, default='frosted', verbose_name="Стиль карточек оригинальной темы")

    # === GIF-тема ===
    background_gif = models.ImageField(upload_to='themes/gifs/', blank=True)
    gif_size = models.CharField(max_length=20, choices=GIF_SIZE_CHOICES, default='contain', verbose_name="Размер GIF")
    gif_position = models.CharField(max_length=20, choices=GIF_POSITION_CHOICES, default='center center', verbose_name="Позиция GIF")
    gif_overlay_opacity = models.CharField(max_length=4, default="0.35", verbose_name="Белая пелена поверх GIF")
    gif_card_transparency = models.CharField(max_length=4, default="0.72", verbose_name="Прозрачность карточек (GIF-тема)")
    gif_card_blur = models.PositiveSmallIntegerField(default=22, verbose_name="Размытие карточек GIF-темы")
    gif_card_style = models.CharField(max_length=20, choices=CARD_STYLE_CHOICES, default='frosted', verbose_name="Стиль карточек GIF-темы")
    gif_text_color = models.CharField(max_length=7, default="#17212b", verbose_name="Текст GIF-темы")
    gif_text_opacity = models.CharField(max_length=4, default="1.0", verbose_name="Прозрачность текста GIF-темы")
    gif_primary_color = models.CharField(max_length=7, default="#229ED9", verbose_name="Акцент GIF-темы")

    # === Аниме-тема ===
    anime_bg_color = models.CharField(max_length=7, default="#fff3f8", verbose_name="Фон (аниме)")
    anime_card_color = models.CharField(max_length=20, default="#ffffff", verbose_name="Цвет карточек (аниме)")
    anime_card_transparency = models.CharField(max_length=4, default="0.86", verbose_name="Прозрачность карточек (аниме)")
    anime_card_blur = models.PositiveSmallIntegerField(default=18, verbose_name="Размытие карточек аниме-темы")
    anime_card_style = models.CharField(max_length=20, choices=CARD_STYLE_CHOICES, default='frosted', verbose_name="Стиль карточек аниме-темы")
    anime_text_color = models.CharField(max_length=7, default="#35222d", verbose_name="Текст (аниме)")
    anime_text_opacity = models.CharField(max_length=4, default="1.0", verbose_name="Прозрачность текста аниме-темы")
    anime_muted_color = models.CharField(max_length=7, default="#8b6577", verbose_name="Вторичный текст (аниме)")
    anime_primary_color = models.CharField(max_length=7, default="#ff7fb3", verbose_name="Акцент (аниме)")
    anime_use_gif = models.BooleanField(default=False, verbose_name="Использовать GIF как фон (аниме)")
    anime_gif_overlay_opacity = models.CharField(max_length=4, default="0.40", verbose_name="Пелена поверх GIF (аниме)")
    anime_gif_size = models.CharField(max_length=20, choices=GIF_SIZE_CHOICES, default='cover', verbose_name="Размер GIF (аниме)")
    anime_gif_position = models.CharField(max_length=20, choices=GIF_POSITION_CHOICES, default='center center', verbose_name="Позиция GIF (аниме)")
    anime_hero_opacity = models.CharField(max_length=4, default="0.18", verbose_name="Прозрачность картинки-героя (аниме)")
    hero_image = models.ImageField(upload_to='themes/heroes/', blank=True)

    # === Деловая тема ===
    business_background_color = models.CharField(max_length=7, default="#e6e9ee", verbose_name="Фон деловой темы")
    business_card_color = models.CharField(max_length=20, default="#f8fafc", verbose_name="Карточки деловой темы")
    business_card_transparency = models.CharField(max_length=4, default="0.62", verbose_name="Прозрачность карточек деловой темы")
    business_card_blur = models.PositiveSmallIntegerField(default=26, verbose_name="Размытие карточек деловой темы")
    business_card_style = models.CharField(max_length=20, choices=CARD_STYLE_CHOICES, default='metallic', verbose_name="Стиль карточек деловой темы")
    business_text_color = models.CharField(max_length=7, default="#1f2937", verbose_name="Текст деловой темы")
    business_text_opacity = models.CharField(max_length=4, default="1.0", verbose_name="Прозрачность текста деловой темы")
    business_muted_color = models.CharField(max_length=7, default="#6b7280", verbose_name="Вторичный текст деловой темы")
    business_primary_color = models.CharField(max_length=7, default="#64748b", verbose_name="Акцент деловой темы")
    business_background_image = models.ImageField(upload_to='themes/business/', blank=True, verbose_name="Фото-фон деловой темы")
    business_background_gif = models.ImageField(upload_to='themes/business/', blank=True, verbose_name="GIF-фон деловой темы")
    business_background_size = models.CharField(max_length=20, choices=GIF_SIZE_CHOICES, default='cover', verbose_name="Размер фона деловой темы")
    business_background_position = models.CharField(max_length=20, choices=GIF_POSITION_CHOICES, default='center center', verbose_name="Позиция фона деловой темы")
    business_overlay_opacity = models.CharField(max_length=4, default="0.45", verbose_name="Светлая пелена деловой темы")
    business_reflection_strength = models.CharField(max_length=4, default="0.24", verbose_name="Сила металлического отражения")

    # === Брендинг и звуки сайта ===
    site_name = models.CharField(max_length=80, default='Zauchka.RU', verbose_name='Название сайта')
    site_logo = models.ImageField(upload_to='site_brand/', blank=True, verbose_name='Фото / логотип сайта')
    send_sound = models.FileField(upload_to='site_sounds/', blank=True, verbose_name='Звук отправки сообщений')
    notification_sound = models.FileField(upload_to='site_sounds/', blank=True, verbose_name='Звук новых сообщений')
    report_sound = models.FileField(upload_to='site_sounds/', blank=True, verbose_name='Звук отправки жалобы')
    support_open_sound = models.FileField(upload_to='site_sounds/', blank=True, verbose_name='Звук открытия окна помощи')
    support_close_sound = models.FileField(upload_to='site_sounds/', blank=True, verbose_name='Звук закрытия окна помощи')
    send_sound_volume = models.PositiveSmallIntegerField(default=100, verbose_name='Громкость отправки, %')
    notification_sound_volume = models.PositiveSmallIntegerField(default=100, verbose_name='Громкость уведомления, %')
    report_sound_volume = models.PositiveSmallIntegerField(default=100, verbose_name='Громкость жалобы, %')
    support_open_sound_volume = models.PositiveSmallIntegerField(default=100, verbose_name='Громкость открытия помощи, %')
    support_close_sound_volume = models.PositiveSmallIntegerField(default=100, verbose_name='Громкость закрытия помощи, %')
    sound_enabled_default = models.BooleanField(default=True, verbose_name='Звук включён по умолчанию')

    # === Виджет обращения к админу ===
    support_widget_gif = models.ImageField(upload_to='themes/support/', blank=True, verbose_name="GIF виджета помощи")
    support_widget_text = models.CharField(max_length=120, default="Привет, буду рад помочь!", verbose_name="Текст виджета помощи")
    support_widget_title = models.CharField(max_length=80, default="Помощь администратора", verbose_name="Заголовок окна помощи")

    def __str__(self):
        return "Настройки тем сайта"


class FavoriteItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_olympiads')
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'olympiad')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} -> {self.olympiad.public_code}'


class SupportThread(models.Model):
    KIND_CHOICES = [
        ('support', 'Вопрос'),
        ('comment_report', 'Жалоба'),
    ]
    STATUS_CHOICES = [
        ('open', 'Открыто'),
        ('closed', 'Закрыто'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_threads')
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default='support')
    subject = models.CharField(max_length=255, default='Вопрос')
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, blank=True, related_name='support_threads')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    @property
    def unread_for_admin(self):
        return self.messages.filter(is_admin=False, read_by_admin=False).count()

    def __str__(self):
        return f'{self.get_kind_display()}: {self.subject}'


class SupportMessage(models.Model):
    thread = models.ForeignKey(SupportThread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='support_messages')
    text = models.TextField(blank=True)
    file = models.FileField(upload_to='support_files/', blank=True)
    is_admin = models.BooleanField(default=False)
    read_by_admin = models.BooleanField(default=False)
    read_by_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def clean(self):
        if self.file and self.file.size > SUPPORT_FILE_LIMIT:
            raise ValidationError('Файл не должен превышать 5 МБ.')

    @property
    def file_name(self):
        return self.file.name.split('/')[-1] if self.file else ''

    @property
    def file_ext(self):
        return self.file_name.rsplit('.', 1)[-1].lower() if '.' in self.file_name else ''

    @property
    def file_is_image(self):
        return self.file_ext in {'jpg','jpeg','png','gif','webp','bmp'}

    @property
    def file_is_video(self):
        return self.file_ext in {'mp4','webm','ogg','mov'}

    def __str__(self):
        sender = self.sender.username if self.sender else 'Система'
        return f'{sender}: {self.text[:40] or "файл"}'
