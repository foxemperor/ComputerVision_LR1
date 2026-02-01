import os
import cv2
import numpy as np


def draw_cross_on_camera():
    """
    Задание 6: Захват изображения с камеры и рисование красного креста
    """
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 6: Изображение с камеры + красный крест")
    print("=" * 60)
    
    # Открываем веб-камеру (0 - первая камера)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Ошибка: не удалось открыть камеру")
        print("Убедитесь, что камера подключена и не используется другим приложением")
        return
    
    # Устанавливаем разрешение (опционально)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"\nКамера инициализирована")
    print(f"   Разрешение: {width}x{height}")
    print("\nУправление:")
    print("   SPACE - сделать снимок и сохранить")
    print("   ESC - выход")
    
    # Параметры креста
    cross_color = (0, 0, 255)  # Красный цвет в BGR
    cross_thickness = 3
    
    # Размеры креста (в пикселях)
    vertical_width = 60    # ширина вертикальной части
    vertical_height = 180  # высота вертикальной части
    horizontal_width = 180  # ширина горизонтальной части
    horizontal_height = 60  # высота горизонтальной части
    
    cv2.namedWindow('Camera with Cross', cv2.WINDOW_NORMAL)
    
    snapshot_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Ошибка: не удалось захватить кадр")
            break
        
        # Создаём копию для рисования
        frame_with_cross = frame.copy()
        
        # Вычисляем центр изображения
        center_x = width // 2
        center_y = height // 2
        
        # Рисуем вертикальную часть креста
        cv2.rectangle(
            frame_with_cross,
            (center_x - vertical_width // 2, center_y - vertical_height // 2),
            (center_x + vertical_width // 2, center_y + vertical_height // 2),
            cross_color,
            cross_thickness
        )
        
        # Рисуем горизонтальную часть креста
        cv2.rectangle(
            frame_with_cross,
            (center_x - horizontal_width // 2, center_y - horizontal_height // 2),
            (center_x + horizontal_width // 2, center_y + horizontal_height // 2),
            cross_color,
            cross_thickness
        )
        
        # Добавляем текст с инструкцией
        cv2.putText(
            frame_with_cross,
            "SPACE - snapshot, ESC - exit",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
        
        # Отображаем
        cv2.imshow('Camera with Cross', frame_with_cross)
        
        # Обработка клавиш
        key = cv2.waitKey(1) & 0xFF
        
        if key == 27:  # ESC
            print("\nВыход из программы")
            break
        elif key == 32:  # SPACE
            snapshot_count += 1
            filename = f"output/camera_snapshot_{snapshot_count}.png"
            cv2.imwrite(filename, frame_with_cross)
            print(f"Снимок сохранён: {filename}")
    
    # Освобождение ресурсов
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\nВсего снимков: {snapshot_count}")


def draw_cross_static_image():
    """
    Альтернатива: Рисование креста на статичном изображении
    (если камера недоступна)
    """
    print("\n" + "=" * 60)
    print("АЛЬТЕРНАТИВА: Крест на статичном изображении")
    print("=" * 60)
    
    image_path = "images/test_image.png"
    
    if not os.path.exists(image_path):
        print(f"Ошибка: файл {image_path} не найден")
        return
    
    # Загружаем изображение
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    if img is None:
        print("Ошибка: не удалось загрузить изображение")
        return
    
    height, width = img.shape[:2]
    center_x = width // 2
    center_y = height // 2
    
    # Параметры креста
    cross_color = (0, 0, 255)  # Красный
    cross_thickness = 3
    
    vertical_width = 60
    vertical_height = 180
    horizontal_width = 180
    horizontal_height = 60
    
    # Рисуем вертикальную часть
    cv2.rectangle(
        img,
        (center_x - vertical_width // 2, center_y - vertical_height // 2),
        (center_x + vertical_width // 2, center_y + vertical_height // 2),
        cross_color,
        cross_thickness
    )
    
    # Рисуем горизонтальную часть
    cv2.rectangle(
        img,
        (center_x - horizontal_width // 2, center_y - horizontal_height // 2),
        (center_x + horizontal_width // 2, center_y + horizontal_height // 2),
        cross_color,
        cross_thickness
    )
    
    # Сохраняем и показываем
    output_path = "output/image_with_cross.png"
    cv2.imwrite(output_path, img)
    
    cv2.namedWindow('Image with Cross', cv2.WINDOW_NORMAL)
    cv2.imshow('Image with Cross', img)
    
    print(f"\nИзображение с крестом создано")
    print(f"Сохранено: {output_path}")
    print("\nНажмите любую клавишу...")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    """
    Главная функция
    """
    print("\n" + "=" * 60)
    print(" ЛАБОРАТОРНАЯ РАБОТА №1 - ЗАДАНИЕ 6")
    print(" Изображение с камеры + красный крест")
    print("=" * 60)
    
    import os
    os.makedirs("output", exist_ok=True)
    
    try:
        # Пробуем работу с камерой
        draw_cross_on_camera()
        
        # Если нужно, можно также сделать статичный вариант
        # print("\n" + "=" * 60)
        # input("\nНажмите Enter для статичного варианта...")
        # draw_cross_static_image()
        
        print("\n" + "=" * 60)
        print("ЗАДАНИЕ 6 ЗАВЕРШЕНО")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nОшибка: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
