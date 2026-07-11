from django.db import migrations, models


def seed_new_builtin_themes(apps, schema_editor):
    ThemePreset = apps.get_model('main', 'ThemePreset')
    presets = [
        ('telegram-light', 'Голубая Telegram', '#eaf6ff', '#ffffff', 'telegram', '#17212b', '#229ED9', 'none', 10),
        ('black-orange', 'Black Orange', '#0b0d10', '#171a20', 'dark_glass', '#fff7ed', '#f97316', 'none', 20),
        ('aqua-ios', 'Aqua iOS', '#dff7ff', '#f8fdff', 'frosted', '#0f2537', '#0ea5e9', 'rain', 30),
        ('pink-soft', 'Pink Soft', '#fff1f7', '#ffffff', 'instagram', '#331827', '#ec4899', 'none', 40),
        ('business', 'Business Metal', '#cfd5dd', '#f3f6f9', 'metallic', '#17202a', '#475569', 'none', 50),
        ('new-year', 'Новый год', '#e9f8ff', '#ffffff', 'frosted', '#102a43', '#0f9f8f', 'snow', 60),
        ('custom', 'Своя тема', '#f7fbff', '#ffffff', 'frosted', '#17212b', '#229ED9', 'none', 90),
    ]
    for key, name, bg, card, style, text, primary, overlay, order in presets:
        obj, _ = ThemePreset.objects.get_or_create(key=key, defaults={'name': name})
        obj.name = name
        obj.is_builtin = True
        obj.sort_order = order
        obj.background_color = bg
        obj.card_color = card
        obj.card_style = style
        obj.text_color = text
        obj.primary_color = primary
        obj.overlay_effect = overlay
        obj.save()
    ThemePreset.objects.filter(key__in=['anime-asuka', 'graphite-glass', 'silver-line', 'gif']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_dynamic_theme_presets_brand_sound'),
    ]

    operations = [
        migrations.AddField(
            model_name='themepreset',
            name='overlay_effect',
            field=models.CharField(choices=[('none', 'Нет'), ('snow', 'Снег'), ('rain', 'Дождь'), ('custom_gif', 'GIF поверх сайта')], default='none', max_length=20),
        ),
        migrations.AddField(
            model_name='themepreset',
            name='overlay_opacity',
            field=models.DecimalField(decimal_places=2, default=0.35, max_digits=3),
        ),
        migrations.AddField(
            model_name='themepreset',
            name='overlay_gif',
            field=models.ImageField(blank=True, upload_to='themes/presets/overlays/'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='report_sound',
            field=models.FileField(blank=True, upload_to='site_sounds/', verbose_name='Звук отправки жалобы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='support_open_sound',
            field=models.FileField(blank=True, upload_to='site_sounds/', verbose_name='Звук открытия окна помощи'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='support_close_sound',
            field=models.FileField(blank=True, upload_to='site_sounds/', verbose_name='Звук закрытия окна помощи'),
        ),
        migrations.RunPython(seed_new_builtin_themes, migrations.RunPython.noop),
    ]
