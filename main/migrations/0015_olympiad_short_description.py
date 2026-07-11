from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_favorites_comment_admin_controls_sound_volume'),
    ]

    operations = [
        migrations.AddField(
            model_name='olympiad',
            name='short_description',
            field=models.CharField(blank=True, max_length=320, verbose_name='Краткое описание'),
        ),
    ]
