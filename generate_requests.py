import json
import time
from decouple import config
import google.generativeai as genai

GOOGLE_API_KEY = config("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")


def generate_message():  # генерим обращения
    prompt = '''Сгенерируй одно реалистичное обращение в службу поддержки по различным проблемам, 
                связанный с заказом еды или доставкой либо с самим заказом, 
                без указания категории и без указании нумерации'''
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Ошибка при генерации сообщения: {e}")
        return "Ошибка генерации"  # Возвращаем сообщение об ошибке

# Загрузка существующих данных из файла final_test.json
try:
    with open("gemini_testing.json", "r", encoding="utf-8") as file:
        requests_data = json.load(file)
except FileNotFoundError:
    requests_data = {}

# Загрузка существующих данных из файла final_test.json
try:
    with open("final_test.json", "r", encoding="utf-8") as file:
        results = json.load(file)
except FileNotFoundError:
    results = {}

batch_number = 10  # Размер партии для генерации

while requests_data:
    batch = {k: requests_data[k] for k in list(requests_data)[:batch_number]}
    messages_generated = False

    for request_id, request_info in batch.items():
        generated_message = generate_message()
        if len(generated_message) > 30:  # Проверяем длину сгенерированного сообщения
            request_info["message"] = generated_message
            time.sleep(2)  # Задержка между запросами
            messages_generated = True

    if not messages_generated:
        print('Не удалось сгенерировать обращение(')

    results.update(batch)

    with open("final_test.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    requests_data = {k: v for k, v in requests_data.items() if k not in batch}

    with open("gemini_testing.json", "w", encoding="utf-8") as file:
        # Обновляем исходный файл с оставшими записями
        json.dump(requests_data, file, indent=4, ensure_ascii=False)

print("Данные добавлены :))")
