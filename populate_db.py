import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olympiad_site.settings')
django.setup()

from main.models import Olympiad
from datetime import date

# Примеры данных
data = [
    {
        "title": "Всероссийская олимпиада школьников (ВОШ) по информатике - Школьный этап (РБ)",
        "link": "https://olimpiada.ru/voz",
        "start_date": date(2024, 9, 1),
        "end_date": date(2025, 10, 15), # Активная
        "target_audience": "school",
        "grade": 9,
        "stage": "municipal",
        "format": "offline",
        "region": "Республика Башкортостан"
    },
    {
        "title": "Олимпиада СПбГУ по праву",
        "link": "https://spbu.ru/",
        "start_date": date(2024, 10, 1),
        "end_date": date(2025, 3, 20), # Активная
        "target_audience": "student",
        "grade": None,
        "stage": "all_russia",
        "format": "online",
        "region": "Россия"
    },
    {
        "title": "Олимпиада МГУ «Ломоносов» по биологии",
        "link": "https://lomonosov.msu.ru/",
        "start_date": date(2023, 10, 1),
        "end_date": date(2024, 2, 15), # ПРОШЕДШАЯ (попадет в архив!)
        "target_audience": "school",
        "grade": 11,
        "stage": "all_russia",
        "format": "online",
        "region": "Россия"
    },
    {
        "title": "Региональный грантовый конкурс для студентов УГАТУ",
        "link": "https://ugatu.ru/",
        "start_date": date(2024, 11, 1),
        "end_date": date(2025, 5, 1), # Активная
        "target_audience": "student",
        "grade": None,
        "stage": "regional",
        "format": "offline",
        "region": "Республика Башкортостан"
    },
    {
        "title": "Олимпиада «Высшая проба» от УрФУ для школьников 10-11 классов",
        "link": "https://urfu.ru/",
        "start_date": date(2024, 12, 1),
        "end_date": date(2025, 4, 10), # Активная
        "target_audience": "school",
        "grade": 10,
        "stage": "regional",
        "format": "online",
        "region": "Россия"
    }
]

# Очищаем старые данные (если запускаешь скрипт второй раз)
Olympiad.objects.all().delete()

# Создаем новые
for item in data:
    Olympiad.objects.create(**item)

print("✅ Примеры олимпиад успешно добавлены в базу!")