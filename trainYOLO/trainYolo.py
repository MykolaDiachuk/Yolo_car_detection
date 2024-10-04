from ultralytics import YOLO
import tensorflow as tf
# Завантажуємо попередньо натреновану модель
model = YOLO('yolov8s.pt')  # Використовуємо найновішу версію моделі YOLOv8

# Тренування моделі

with tf.device('/GPU:0'):
    model.train(data=r'C:\Users\PC\PycharmProjects\Yolo_car_detection\trainYOLO\data.yaml', epochs=10, batch=5, imgsz=640,save_dir='trainYOLO')