from django.db import migrations, models


def seed_theme_presets(apps, schema_editor):
    ThemePreset = apps.get_model('main', 'ThemePreset')
    defaults = [
        {'key':'telegram-light','name':'Голубая белая','is_builtin':True,'sort_order':10,'background_color':'#eef6fb','card_color':'#ffffff','card_transparency':'0.88','card_blur':18,'card_style':'telegram','text_color':'#17212b','muted_color':'#657786','primary_color':'#229ED9'},
        {'key':'custom','name':'Оригинальная','is_builtin':True,'sort_order':20,'background_color':'#f7fbff','card_color':'#ffffff','card_transparency':'0.92','card_blur':16,'card_style':'frosted','text_color':'#17212b','muted_color':'#657786','primary_color':'#229ED9'},
        {'key':'gif','name':'GIF-тема','is_builtin':True,'sort_order':30,'background_color':'#eef6fb','card_color':'#ffffff','card_transparency':'0.70','card_blur':24,'card_style':'frosted','background_size':'contain','text_color':'#17212b','muted_color':'#657786','primary_color':'#229ED9'},
        {'key':'business','name':'Деловой стиль','is_builtin':True,'sort_order':40,'background_color':'#d8dde5','card_color':'#f8fafc','card_transparency':'0.58','card_blur':28,'card_style':'metallic','text_color':'#1f2937','muted_color':'#64748b','primary_color':'#64748b','reflection_strength':'0.25','card_shadow_opacity':'0.18'},
        {'key':'graphite-glass','name':'Graphite Glass','is_builtin':True,'sort_order':50,'background_color':'#111827','card_color':'#1f2937','card_transparency':'0.62','card_blur':28,'card_style':'dark_glass','text_color':'#f9fafb','muted_color':'#9ca3af','primary_color':'#60a5fa'},
        {'key':'silver-line','name':'Silver Line','is_builtin':True,'sort_order':60,'background_color':'#edf1f5','card_color':'#f8fafc','card_transparency':'0.76','card_blur':22,'card_style':'soft','text_color':'#17212b','muted_color':'#6b7280','primary_color':'#475569'},
    ]
    for data in defaults:
        ThemePreset.objects.get_or_create(key=data['key'], defaults=data)
    ThemePreset.objects.filter(key='anime-asuka').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_olympiad_codes_unified_card_theme'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThemePreset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.SlugField(max_length=64, unique=True)),
                ('name', models.CharField(default='Новая тема', max_length=80)),
                ('is_builtin', models.BooleanField(default=False)),
                ('sort_order', models.PositiveSmallIntegerField(default=100)),
                ('font_family', models.CharField(blank=True, default='Inter', max_length=120)),
                ('base_font_size', models.PositiveSmallIntegerField(default=16)),
                ('interface_scale', models.DecimalField(decimal_places=2, default=1.25, max_digits=3)),
                ('background_color', models.CharField(default='#eef6fb', max_length=7)),
                ('background_image', models.ImageField(blank=True, upload_to='themes/presets/images/')),
                ('background_gif', models.ImageField(blank=True, upload_to='themes/presets/gifs/')),
                ('background_size', models.CharField(choices=[('cover', 'Заполнить'), ('contain', 'Показать полностью'), ('100% auto', 'По ширине'), ('auto 100%', 'По высоте'), ('auto', 'Оригинальный размер')], default='cover', max_length=20)),
                ('background_position', models.CharField(choices=[('center center', 'Центр'), ('center top', 'Верх'), ('center bottom', 'Низ'), ('left center', 'Слева'), ('right center', 'Справа')], default='center center', max_length=20)),
                ('background_opacity', models.DecimalField(decimal_places=2, default=1.0, max_digits=3)),
                ('card_color', models.CharField(default='#ffffff', max_length=7)),
                ('card_transparency', models.DecimalField(decimal_places=2, default=0.88, max_digits=3)),
                ('card_blur', models.PositiveSmallIntegerField(default=18)),
                ('card_style', models.CharField(choices=[('frosted', 'Размытое стекло'), ('solid', 'Плотная карточка'), ('soft', 'Мягкая светлая'), ('outline', 'Контурная'), ('metallic', 'Серый металлик'), ('dark_glass', 'Тёмное стекло'), ('telegram', 'Telegram clean'), ('discord', 'Discord panel'), ('instagram', 'Instagram soft')], default='frosted', max_length=20)),
                ('card_border_opacity', models.DecimalField(decimal_places=2, default=0.24, max_digits=3)),
                ('card_shadow_opacity', models.DecimalField(decimal_places=2, default=0.12, max_digits=3)),
                ('reflection_strength', models.DecimalField(decimal_places=2, default=0.25, max_digits=3)),
                ('text_color', models.CharField(default='#17212b', max_length=7)),
                ('text_opacity', models.DecimalField(decimal_places=2, default=1.0, max_digits=3)),
                ('muted_color', models.CharField(default='#657786', max_length=7)),
                ('primary_color', models.CharField(default='#229ED9', max_length=7)),
                ('danger_color', models.CharField(default='#e0245e', max_length=7)),
                ('custom_css', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['sort_order', 'name']},
        ),
        migrations.AddField('customtheme', 'site_name', models.CharField(default='Zauchka.RU', max_length=80, verbose_name='Название сайта')),
        migrations.AddField('customtheme', 'site_logo', models.ImageField(blank=True, upload_to='site_brand/', verbose_name='Фото / логотип сайта')),
        migrations.AddField('customtheme', 'send_sound', models.FileField(blank=True, upload_to='site_sounds/', verbose_name='Звук отправки сообщений')),
        migrations.AddField('customtheme', 'notification_sound', models.FileField(blank=True, upload_to='site_sounds/', verbose_name='Звук новых сообщений')),
        migrations.AddField('customtheme', 'sound_enabled_default', models.BooleanField(default=True, verbose_name='Звук включён по умолчанию')),
        migrations.RunPython(seed_theme_presets, migrations.RunPython.noop),
    ]
