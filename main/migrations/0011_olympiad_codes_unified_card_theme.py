from django.db import migrations, models


def fill_public_numbers(apps, schema_editor):
    Olympiad = apps.get_model('main', 'Olympiad')
    used = set(Olympiad.objects.exclude(public_number__isnull=True).values_list('public_number', flat=True))
    next_number = 0
    for olympiad in Olympiad.objects.filter(public_number__isnull=True).order_by('id'):
        while next_number in used:
            next_number += 1
        olympiad.public_number = next_number
        olympiad.save(update_fields=['public_number'])
        used.add(next_number)
        next_number += 1


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_admin_theme_online_chat_improvements'),
    ]

    operations = [
        migrations.AddField(
            model_name='olympiad',
            name='public_number',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name='Номер карточки'),
        ),
        migrations.AddField(
            model_name='olympiad',
            name='listing_type',
            field=models.CharField(choices=[('olympiad', 'Олимпиада'), ('grant', 'Грант')], default='olympiad', max_length=12, verbose_name='Тип'),
        ),
        migrations.AddField(
            model_name='olympiad',
            name='organizer',
            field=models.CharField(blank=True, max_length=255, verbose_name='Организатор'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='telegram_card_blur',
            field=models.PositiveSmallIntegerField(default=18, verbose_name='Размытие карточек голубой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='telegram_card_style',
            field=models.CharField(choices=[('frosted', 'Размытое стекло'), ('solid', 'Непрозрачные карточки'), ('outline', 'Тонкая рамка без заливки'), ('metallic', 'Серый металлик'), ('dark_glass', 'Тёмное стекло')], default='frosted', max_length=20, verbose_name='Стиль карточек голубой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='custom_card_blur',
            field=models.PositiveSmallIntegerField(default=18, verbose_name='Размытие карточек оригинальной темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='custom_card_style',
            field=models.CharField(choices=[('frosted', 'Размытое стекло'), ('solid', 'Непрозрачные карточки'), ('outline', 'Тонкая рамка без заливки'), ('metallic', 'Серый металлик'), ('dark_glass', 'Тёмное стекло')], default='frosted', max_length=20, verbose_name='Стиль карточек оригинальной темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='gif_card_blur',
            field=models.PositiveSmallIntegerField(default=22, verbose_name='Размытие карточек GIF-темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='gif_card_style',
            field=models.CharField(choices=[('frosted', 'Размытое стекло'), ('solid', 'Непрозрачные карточки'), ('outline', 'Тонкая рамка без заливки'), ('metallic', 'Серый металлик'), ('dark_glass', 'Тёмное стекло')], default='frosted', max_length=20, verbose_name='Стиль карточек GIF-темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='anime_card_blur',
            field=models.PositiveSmallIntegerField(default=18, verbose_name='Размытие карточек аниме-темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='anime_card_style',
            field=models.CharField(choices=[('frosted', 'Размытое стекло'), ('solid', 'Непрозрачные карточки'), ('outline', 'Тонкая рамка без заливки'), ('metallic', 'Серый металлик'), ('dark_glass', 'Тёмное стекло')], default='frosted', max_length=20, verbose_name='Стиль карточек аниме-темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='business_card_blur',
            field=models.PositiveSmallIntegerField(default=26, verbose_name='Размытие карточек деловой темы'),
        ),
        migrations.AddField(
            model_name='customtheme',
            name='business_card_style',
            field=models.CharField(choices=[('frosted', 'Размытое стекло'), ('solid', 'Непрозрачные карточки'), ('outline', 'Тонкая рамка без заливки'), ('metallic', 'Серый металлик'), ('dark_glass', 'Тёмное стекло')], default='metallic', max_length=20, verbose_name='Стиль карточек деловой темы'),
        ),
        migrations.RunPython(fill_public_numbers, migrations.RunPython.noop),
    ]
