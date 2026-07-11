from pathlib import Path
p=Path('/mnt/data/work10/main/models.py')
s=p.read_text()
# imports not needed
s=s.replace("    cookies_agreement = models.BooleanField(default=False, verbose_name=\"Согласие на Cookies\")\n", "    cookies_agreement = models.BooleanField(default=False, verbose_name=\"Согласие на Cookies\")\n    can_upload_photo = models.BooleanField(default=True, verbose_name=\"Может менять фото профиля\")\n    can_change_username = models.BooleanField(default=True, verbose_name=\"Может менять имя аккаунта\")\n    can_comment = models.BooleanField(default=True, verbose_name=\"Может писать комментарии\")\n")
s=s.replace("    is_approved = models.BooleanField(default=True)\n\n    @property\n    def html_text(self):", "    is_approved = models.BooleanField(default=True)\n    is_deleted = models.BooleanField(default=False, verbose_name='Удалён администратором')\n    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_deleted_comments')\n    deleted_at = models.DateTimeField(null=True, blank=True)\n    delete_reason = models.TextField(blank=True)\n    show_delete_notice = models.BooleanField(default=True, verbose_name='Показывать окно удаления')\n\n    @property\n    def html_text(self):")
s=s.replace("    notification_sound = models.FileField(upload_to='site_sounds/', blank=True, verbose_name='Звук новых сообщений')\n    report_sound = models.FileField(upload_to='site_sounds/', blank=True, verbose_name='Звук отправки жалобы')\n    support_open_sound = models.FileField(upload_to='site_sounds/', blank=True, verbose_name='Звук открытия окна помощи')\n    support_close_sound = models.FileField(upload_to='site_sounds/', blank=True, verbose_name='Звук закрытия окна помощи')\n    sound_enabled_default = models.BooleanField(default=True, verbose_name='Звук включён по умолчанию')\n", "    notification_sound = models.FileField(upload_to='site_sounds/', blank=True, verbose_name='Звук новых сообщений')\n    report_sound = models.FileField(upload_to='site_sounds/', blank=True, verbose_name='Звук отправки жалобы')\n    support_open_sound = models.FileField(upload_to='site_sounds/', blank=True, verbose_name='Звук открытия окна помощи')\n    support_close_sound = models.FileField(upload_to='site_sounds/', blank=True, verbose_name='Звук закрытия окна помощи')\n    send_sound_volume = models.PositiveSmallIntegerField(default=100, verbose_name='Громкость отправки, %')\n    notification_sound_volume = models.PositiveSmallIntegerField(default=100, verbose_name='Громкость уведомления, %')\n    report_sound_volume = models.PositiveSmallIntegerField(default=100, verbose_name='Громкость жалобы, %')\n    support_open_sound_volume = models.PositiveSmallIntegerField(default=100, verbose_name='Громкость открытия помощи, %')\n    support_close_sound_volume = models.PositiveSmallIntegerField(default=100, verbose_name='Громкость закрытия помощи, %')\n    sound_enabled_default = models.BooleanField(default=True, verbose_name='Звук включён по умолчанию')\n")
insert = """

class FavoriteItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_olympiads')
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'olympiad')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} -> {self.olympiad.public_code}'
"""
# Insert FavoriteItem before SupportThread
s=s.replace("\n\nclass SupportThread(models.Model):", insert+"\n\nclass SupportThread(models.Model):")
p.write_text(s)
