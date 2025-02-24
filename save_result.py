import json
import re

with open('category_result_test_final.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

category_count = {}

for entry in data.values():
    # Получаем категории, разбиваем по символу новой строки
    categories = entry['category'].split('\n')

    for category in categories:
        # Убираем префиксы и лишние пробелы с помощью регулярного выражения
        category = re.sub(r'^[\*\d\.]+\s*', '', category)  # Удаляем префиксы с цифрами, точками и звездочками
        category = re.sub(r'[\*\s]+$', '', category)  # Удаляем звездочки и пробелы в конце строки
        category = category.strip()

        # Если категория не пустая, увеличиваем счетчик
        if category:  # Проверяем, что категория не пустая
            if category in category_count:
                category_count[category] += 1
            else:
                category_count[category] = 1

# Сохраняем результат в файл
with open('result_final.json', 'w', encoding='utf-8') as file:
    json.dump(category_count, file, ensure_ascii=False, indent=4)

print("Данные сохранены в файл result_final4.json")