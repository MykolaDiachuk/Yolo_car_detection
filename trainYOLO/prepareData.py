import json
import os
import random

# Директорії з JSON-файлами та немаркованими зображеннями
json_dir = r'C:\Users\PC\PycharmProjects\new video&photo\OutputDir'  # Промарковані JSON файли
unlabeled_images_dir = r"C:\Users\PC\PycharmProjects\new video&photo\photo for dataset\no_cars"  # Папка з немаркованими зображеннями

# Директорії для збереження тренувальних та валідаційних txt файлів
train_output_dir = r'C:\Users\PC\PycharmProjects\AMA_many_car_object_detection\trainYOLO\dataset\labels\train'
val_output_dir = r'C:\Users\PC\PycharmProjects\AMA_many_car_object_detection\trainYOLO\dataset\labels\val'

os.makedirs(train_output_dir, exist_ok=True)
os.makedirs(val_output_dir, exist_ok=True)

# Встановлення пропорцій розділення (наприклад, 80% на тренування, 20% на валідацію)
train_ratio = 0.8

# Отримуємо список всіх JSON-файлів
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

# Отримуємо список всіх немаркованих зображень
unlabeled_image_files = [f for f in os.listdir(unlabeled_images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]

# Розмішуємо файли випадковим чином
random.shuffle(json_files)
random.shuffle(unlabeled_image_files)

# Визначаємо кількість файлів для тренування
train_count = int(len(json_files) * train_ratio)

# Розділяємо файли на тренувальні та валідаційні
train_files = json_files[:train_count]
val_files = json_files[train_count:]

# Ділимо немарковані зображення на тренувальні та валідаційні
unlabeled_train_count = int(len(unlabeled_image_files) * train_ratio)
unlabeled_train_files = unlabeled_image_files[:unlabeled_train_count]
unlabeled_val_files = unlabeled_image_files[unlabeled_train_count:]

# Функція для конвертації JSON у формат YOLO та запису у відповідний txt файл
def convert_and_save(files, output_dir):
    for json_file in files:
        json_file_path = os.path.join(json_dir, json_file)

        # Відкриваємо JSON-файл та зчитуємо його вміст
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        # Отримуємо розміри зображення
        image_height = data['imageHeight']
        image_width = data['imageWidth']

        # Створюємо відповідний txt файл для збереження координат об'єктів
        label_file_name = os.path.splitext(json_file)[0] + '.txt'
        label_file_path = os.path.join(output_dir, label_file_name)

        # Записуємо bounding boxes у форматі YOLO
        with open(label_file_path, 'w') as label_f:
            for shape in data['shapes']:
                label = shape['label']  # Назва класу

                # Обчислення центральних координат та розмірів об'єкта
                x_min, y_min = shape['points'][0]
                x_max, y_max = shape['points'][1]

                # Нормалізація координат
                x_center = (x_min + x_max) / 2 / image_width
                y_center = (y_min + y_max) / 2 / image_height
                width = (x_max - x_min) / image_width
                height = (y_max - y_min) / image_height

                # Перевірка та коригування значень, якщо вони виходять за межі [0, 1]
                x_center = max(0, min(x_center, 1))
                y_center = max(0, min(y_center, 1))
                width = max(0, min(width, 1))
                height = max(0, min(height, 1))

                # Клас об'єкта (наприклад, 0 для car, якщо car є єдиним класом)
                class_id = 0  # Змінити на індекс класу, якщо є декілька класів

                # Перевірка на коректність значень перед записом
                if width > 0 and height > 0:
                    # Записуємо у форматі: class x_center y_center width height
                    label_f.write(f'{class_id} {x_center} {y_center} {width} {height}\n')

        print(f"Створено файл: {label_file_path}")

# Функція для створення порожніх txt файлів для немаркованих зображень
def create_empty_txt_files(image_files, output_dir):
    for image_file in image_files:
        # Створюємо відповідний txt файл без вмісту (порожній)
        label_file_name = os.path.splitext(image_file)[0] + '.txt'
        label_file_path = os.path.join(output_dir, label_file_name)
        with open(label_file_path, 'w') as label_f:
            pass  # Створюємо порожній файл

        print(f"Створено порожній файл: {label_file_path}")

# Конвертація тренувальних та валідаційних файлів
convert_and_save(train_files, train_output_dir)
convert_and_save(val_files, val_output_dir)

# Створення порожніх txt файлів для немаркованих зображень
create_empty_txt_files(unlabeled_train_files, train_output_dir)
create_empty_txt_files(unlabeled_val_files, val_output_dir)
