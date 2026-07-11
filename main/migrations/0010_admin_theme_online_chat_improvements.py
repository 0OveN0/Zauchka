from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_support_threads_business_theme_and_widget'),
    ]

    operations = [
        migrations.AddField(
            model_name='olympiad',
            name='cover_image',
            field=models.ImageField(blank=True, upload_to='olympiad_covers/', verbose_name='Обложка'),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_activity',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Последняя активность'),
        ),
        migrations.AddField(
            model_name='profile',
            name='show_online_status',
            field=models.BooleanField(default=True, verbose_name='Показывать онлайн-статус'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='anime_text_opacity',
            field=models.CharField(default='1.0', max_length=4, verbose_name='Прозрачность текста аниме-темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='base_font_size',
            field=models.PositiveSmallIntegerField(default=16, verbose_name='Размер шрифта сайта'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='business_text_opacity',
            field=models.CharField(default='1.0', max_length=4, verbose_name='Прозрачность текста деловой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='custom_background_gif',
            field=models.ImageField(blank=True, upload_to='themes/custom/', verbose_name='GIF-фон оригинальной темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='custom_background_position',
            field=models.CharField(choices=[('center center', 'По центру'), ('center top', 'Сверху по центру'), ('center bottom', 'Снизу по центру'), ('left center', 'Слева по центру'), ('right center', 'Справа по центру')], default='center center', max_length=20, verbose_name='Позиция фона оригинальной темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='custom_background_size',
            field=models.CharField(choices=[('contain', 'Показывать полностью'), ('cover', 'Заполнить весь экран'), ('100% auto', 'Растянуть по ширине'), ('auto 100%', 'Растянуть по высоте')], default='cover', max_length=20, verbose_name='Размер фона оригинальной темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='custom_overlay_opacity',
            field=models.CharField(default='0.18', max_length=4, verbose_name='Прозрачность пелены оригинальной темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='gif_primary_color',
            field=models.CharField(default='#229ED9', max_length=7, verbose_name='Акцент GIF-темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='gif_text_color',
            field=models.CharField(default='#17212b', max_length=7, verbose_name='Текст GIF-темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='gif_text_opacity',
            field=models.CharField(default='1.0', max_length=4, verbose_name='Прозрачность текста GIF-темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='interface_scale',
            field=models.CharField(default='1.0', max_length=4, verbose_name='Масштаб версии покрупнее'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='support_widget_title',
            field=models.CharField(default='Помощь администратора', max_length=80, verbose_name='Заголовок окна помощи'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='telegram_background_gif',
            field=models.ImageField(blank=True, upload_to='themes/telegram/', verbose_name='GIF-фон голубой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='telegram_background_image',
            field=models.ImageField(blank=True, upload_to='themes/telegram/', verbose_name='Фото-фон голубой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='telegram_background_position',
            field=models.CharField(choices=[('center center', 'По центру'), ('center top', 'Сверху по центру'), ('center bottom', 'Снизу по центру'), ('left center', 'Слева по центру'), ('right center', 'Справа по центру')], default='center center', max_length=20, verbose_name='Позиция фона голубой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='telegram_background_size',
            field=models.CharField(choices=[('contain', 'Показывать полностью'), ('cover', 'Заполнить весь экран'), ('100% auto', 'Растянуть по ширине'), ('auto 100%', 'Растянуть по высоте')], default='cover', max_length=20, verbose_name='Размер фона голубой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='telegram_overlay_opacity',
            field=models.CharField(default='0.18', max_length=4, verbose_name='Прозрачность пелены голубой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='telegram_text_opacity',
            field=models.CharField(default='1.0', max_length=4, verbose_name='Прозрачность текста голубой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='text_opacity',
            field=models.CharField(default='1.0', max_length=4, verbose_name='Прозрачность текста оригинальной темы'),
        ),
        migrations.AddField(
            model_name='supportmessage',
            name='read_by_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='supportmessage',
            name='read_by_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='supportthread',
            name='kind',
            field=models.CharField(choices=[('support', 'Вопрос'), ('comment_report', 'Жалоба')], default='support', max_length=20),
        ),
        migrations.AlterField(
            model_name='supportthread',
            name='subject',
            field=models.CharField(default='Вопрос', max_length=255),
        ),
    ]
