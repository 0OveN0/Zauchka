from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_theme_overlay_sounds_admin_media'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='can_upload_photo',
            field=models.BooleanField(default=True, verbose_name='Может менять фото профиля'),
        ),
        migrations.AddField(
            model_name='profile',
            name='can_change_username',
            field=models.BooleanField(default=True, verbose_name='Может менять имя аккаунта'),
        ),
        migrations.AddField(
            model_name='profile',
            name='can_comment',
            field=models.BooleanField(default=True, verbose_name='Может писать комментарии'),
        ),
        migrations.AddField(
            model_name='comment',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Удалён администратором'),
        ),
        migrations.AddField(
            model_name='comment',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='delete_reason',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='show_delete_notice',
            field=models.BooleanField(default=True, verbose_name='Показывать окно удаления'),
        ),
        migrations.AddField(
            model_name='comment',
            name='deleted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin_deleted_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='send_sound_volume',
            field=models.PositiveSmallIntegerField(default=100, verbose_name='Громкость отправки, %'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='notification_sound_volume',
            field=models.PositiveSmallIntegerField(default=100, verbose_name='Громкость уведомления, %'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='report_sound_volume',
            field=models.PositiveSmallIntegerField(default=100, verbose_name='Громкость жалобы, %'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='support_open_sound_volume',
            field=models.PositiveSmallIntegerField(default=100, verbose_name='Громкость открытия помощи, %'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='support_close_sound_volume',
            field=models.PositiveSmallIntegerField(default=100, verbose_name='Громкость закрытия помощи, %'),
        ),
        migrations.CreateModel(
            name='FavoriteItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('olympiad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to='main.olympiad')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_olympiads', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at'], 'unique_together': {('user', 'olympiad')}},
        ),
    ]
