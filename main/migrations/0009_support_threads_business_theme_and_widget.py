# Generated manually for theme editor, business theme and support threads.

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_customtheme_anime_bg_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customtheme',
            name='telegram_background_color',
            field=models.CharField(default='#eef6fb', max_length=7, verbose_name='Фон голубой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='telegram_card_color',
            field=models.CharField(default='#ffffff', max_length=20, verbose_name='Карточки голубой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='telegram_card_transparency',
            field=models.CharField(default='0.88', max_length=4, verbose_name='Прозрачность карточек голубой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='telegram_text_color',
            field=models.CharField(default='#17212b', max_length=7, verbose_name='Текст голубой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='telegram_muted_color',
            field=models.CharField(default='#657786', max_length=7, verbose_name='Вторичный текст голубой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='telegram_primary_color',
            field=models.CharField(default='#229ED9', max_length=7, verbose_name='Акцент голубой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='business_background_color',
            field=models.CharField(default='#e6e9ee', max_length=7, verbose_name='Фон деловой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='business_card_color',
            field=models.CharField(default='#f8fafc', max_length=20, verbose_name='Карточки деловой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='business_card_transparency',
            field=models.CharField(default='0.92', max_length=4, verbose_name='Прозрачность карточек деловой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='business_text_color',
            field=models.CharField(default='#1f2937', max_length=7, verbose_name='Текст деловой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='business_muted_color',
            field=models.CharField(default='#6b7280', max_length=7, verbose_name='Вторичный текст деловой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='business_primary_color',
            field=models.CharField(default='#64748b', max_length=7, verbose_name='Акцент деловой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='business_background_image',
            field=models.ImageField(blank=True, upload_to='themes/business/', verbose_name='Фото-фон деловой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='business_background_gif',
            field=models.ImageField(blank=True, upload_to='themes/business/', verbose_name='GIF-фон деловой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='business_background_size',
            field=models.CharField(choices=[('contain', 'Показывать полностью'), ('cover', 'Заполнить весь экран'), ('100% auto', 'Растянуть по ширине'), ('auto 100%', 'Растянуть по высоте')], default='cover', max_length=20, verbose_name='Размер фона деловой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='business_background_position',
            field=models.CharField(choices=[('center center', 'По центру'), ('center top', 'Сверху по центру'), ('center bottom', 'Снизу по центру'), ('left center', 'Слева по центру'), ('right center', 'Справа по центру')], default='center center', max_length=20, verbose_name='Позиция фона деловой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='business_overlay_opacity',
            field=models.CharField(default='0.45', max_length=4, verbose_name='Светлая пелена деловой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='business_reflection_strength',
            field=models.CharField(default='0.24', max_length=4, verbose_name='Сила металлического отражения'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='support_widget_gif',
            field=models.ImageField(blank=True, upload_to='themes/support/', verbose_name='GIF виджета помощи'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='support_widget_text',
            field=models.CharField(default='Привет, буду рад помочь!', max_length=120, verbose_name='Текст виджета помощи'),
        ),
        migrations.AlterField(
            model_name='customtheme',
            name='font_family',
            field=models.CharField(blank=True, default='Inter', max_length=120, verbose_name='Шрифт всего сайта'),
        ),
        migrations.CreateModel(
            name='SupportThread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('support', 'Обращение'), ('comment_report', 'Жалоба на комментарий')], default='support', max_length=20)),
                ('subject', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('open', 'Открыто'), ('closed', 'Закрыто')], default='open', max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='support_threads', to='main.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='support_threads', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='SupportMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
                ('file', models.FileField(blank=True, upload_to='support_files/')),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='support_messages', to=settings.AUTH_USER_MODEL)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='main.supportthread')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
