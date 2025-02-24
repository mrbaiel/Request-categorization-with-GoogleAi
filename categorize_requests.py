import json
import time
from collections import Counter
from decouple import config
import google.generativeai as genai

GOOGLE_API_KEY = config("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Загрузка данных из исходного файла где лежать наши данные
try:
    with open("final_test.json", "r", encoding="utf-8") as file:
        requests_data = json.load(file)
except FileNotFoundError:
    requests_data = {}  # Если файл не найден, инициализируем пустой словарь

# Загрузка существующих результатов из category_result_test_final.json
try:
    with open("category_result_test_final.json", "r", encoding="utf-8") as file:
        existing_results = json.load(file)
except FileNotFoundError:
    existing_results = {}  # Если файл не найден, инициализируем пустой словарь

def categorize_message(message):
    prompt = f"""Определи категорию только первого обращения в одну из следующих:
    Проблема с доставкой
    Качество еды
    Отмененный или отсутствующий заказ
    Несоответствие заказа
    Запросы на возмещение
    Жалобы на сервис
    Проблема с оплатой
    Технические проблемы
    Проблемы с промокодами
    Проблемы с отслеживанием заказа
    Другое

    Если сообщение не подходит под указанные категории, используй 'Другое'.

    Обращение: "{message}"

    Отвечай только названием категории без дополнительных пояснений и без нумераций
    """
    response = model.generate_content(prompt)
    return response.text.strip()

all_results = {}  # Новый словарь для хранения всех результатов
batch_size = 10  # Размер партии для обработки т.к. залпом отдать на обработку-неэффективно

while requests_data:
    batch = {k: requests_data[k] for k in list(requests_data)[:batch_size]}
    categories = []

    for request_id, request_info in batch.items():
        message = request_info.get("message", "").strip()
        if message:
            category = categorize_message(message)
            categories.append(category)
            request_info["category"] = category
            all_results[request_id] = request_info
            time.sleep(3)  # Задержка между запросами так как без задержки получаем ошибку сервера

    # Записываем все результаты в файл
    filename = "category_result_test_final.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(all_results, file, indent=4, ensure_ascii=False)

    # Удаляем обработанные записи из исходного списка
    requests_data = {k: v for k, v in requests_data.items() if k not in batch}

    # Обновляем исходный файл с оставшимися записями
    with open("final_test.json", "w", encoding="utf-8") as file:
        json.dump(requests_data, file, indent=4, ensure_ascii=False)

print(f"результаты сохранены в {filename}")