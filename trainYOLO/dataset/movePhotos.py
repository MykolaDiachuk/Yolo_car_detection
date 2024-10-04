import os
import shutil

# Шляхи до папок з маркуванням і зображеннями
labels_train_dir = r'C:\Users\PC\PycharmProjects\AMA_many_car_object_detection\trainYOLO\dataset\labels\train'
labels_val_dir = r'C:\Users\PC\PycharmProjects\AMA_many_car_object_detection\trainYOLO\dataset\labels\val'
images_dir = r"C:\Users\PC\PycharmProjects\new video&photo\photo for dataset\no_cars"

# Шляхи для збереження тренувальних та валідаційних зображень
train_images_dir = r'C:\Users\PC\PycharmProjects\AMA_many_car_object_detection\trainYOLO\dataset\images\train'
val_images_dir = r'C:\Users\PC\PycharmProjects\AMA_many_car_object_detection\trainYOLO\dataset\images\val'

# Створення директорій, якщо вони не існують
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)

# Функція для копіювання зображень у відповідні папки
def move_images(label_dir, dest_img_dir):
    # Проходимося по всіх файлах у директорії маркування (наприклад, labels/train або labels/val)
    for label_file in os.listdir(label_dir):
        # Отримуємо ім'я файлу без розширення (наприклад, 'image1' із 'image1.txt')
        base_name = os.path.splitext(label_file)[0]

        # Відповідне зображення повинне мати той самий базовий нейм
        # Додаємо відповідне розширення (наприклад, '.jpg' або '.png')
        image_file = base_name + '.jpg'  # Змінити розширення на відповідне до ваших зображень, якщо потрібно

        # Шлях до оригінального зображення
        src_image_path = os.path.join(images_dir, image_file)
        # Шлях для збереження зображення у відповідній папці (train або val)
        dest_image_path = os.path.join(dest_img_dir, image_file)

        # Якщо зображення існує, копіюємо його в цільову папку
        if os.path.exists(src_image_path):
            shutil.copy(src_image_path, dest_image_path)
            print(f'Копіювання: {src_image_path} -> {dest_image_path}')
        else:
            print(f'Зображення {src_image_path} не знайдено!')

# Копіювання зображень у папку train на основі файлів розмітки
move_images(labels_train_dir, train_images_dir)

# Копіювання зображень у папку val на основі файлів розмітки
move_images(labels_val_dir, val_images_dir)

print("Копіювання завершено.")
