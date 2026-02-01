import cv2
import os
import numpy as np


def explain_hsv():
    """
    Объяснение формата HSV
    """
    print("\n" + "=" * 60)
    print(" ЦВЕТОВАЯ МОДЕЛЬ HSV")
    print("=" * 60)
    print("""
HSV - цветовая модель, где:

    H (Hue) - Оттенок/Тон
       Диапазон: 0-179 в OpenCV (0-360° на цветовом круге)
       Определяет сам цвет
    
    S (Saturation) - Насыщенность
       Диапазон: 0-255
       0 = ненасыщенный (серый), 255 = максимальная насыщенность
    
    V (Value) - Яркость
       Диапазон: 0-255
       0 = чёрный, 255 = максимальная яркость

Преимущества HSV:
   - Упрощённое выделение объектов по цвету
   - Устойчивость к изменениям освещения
   - Разделение цветовой информации и яркости
""")
    print("=" * 60)


def show_image_bgr_and_hsv():
    """
    Задание 5: Отображение изображения в BGR и HSV форматах
    """
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 5: Сравнение BGR и HSV форматов")
    print("=" * 60)
    
    image_path = "images/test_image.png"
    
    if not os.path.exists(image_path):
        print(f"Ошибка: файл {image_path} не найден")
        return
    
    # Загрузка изображения в BGR
    img_bgr = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    if img_bgr is None:
        print("Ошибка: не удалось загрузить изображение")
        return
    
    print(f"\nИсходное изображение (BGR):")
    print(f"   Размер: {img_bgr.shape}")
    print(f"   Тип данных: {img_bgr.dtype}")
    
    # Конвертация в HSV
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    
    print(f"\nИзображение в формате HSV:")
    print(f"   Размер: {img_hsv.shape}")
    print(f"   Тип данных: {img_hsv.dtype}")
    
    # Создание окон
    cv2.namedWindow('Original (BGR)', cv2.WINDOW_NORMAL)
    cv2.namedWindow('HSV Format', cv2.WINDOW_NORMAL)
    
    # Позиционирование окон
    cv2.moveWindow('Original (BGR)', 100, 100)
    cv2.moveWindow('HSV Format', 750, 100)
    
    # Отображение
    cv2.imshow('Original (BGR)', img_bgr)
    cv2.imshow('HSV Format', img_hsv)
    
    print("\nОкна отображены.")
    print("Нажмите любую клавишу для продолжения...")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_hsv_channels_separately():
    """
    Дополнительно: Раздельное отображение каналов HSV
    """
    print("\n" + "=" * 60)
    print("ДОПОЛНИТЕЛЬНО: Раздельные каналы HSV")
    print("=" * 60)
    
    image_path = "images/test_image.png"
    
    if not os.path.exists(image_path):
        print(f"Ошибка: файл {image_path} не найден")
        return
    
    img_bgr = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    if img_bgr is None:
        print("Ошибка: не удалось загрузить изображение")
        return
    
    # Конвертация в HSV
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    
    # Разделение на каналы
    h, s, v = cv2.split(img_hsv)
    
    print("\nСтатистика по каналам:")
    print(f"   H (Hue):        min={h.min()}, max={h.max()}, mean={h.mean():.1f}")
    print(f"   S (Saturation): min={s.min()}, max={s.max()}, mean={s.mean():.1f}")
    print(f"   V (Value):      min={v.min()}, max={v.max()}, mean={v.mean():.1f}")
    
    # Создание окон
    cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
    cv2.namedWindow('H - Hue', cv2.WINDOW_NORMAL)
    cv2.namedWindow('S - Saturation', cv2.WINDOW_NORMAL)
    cv2.namedWindow('V - Value', cv2.WINDOW_NORMAL)
    
    # Позиционирование окон (сетка 2x2)
    cv2.moveWindow('Original', 50, 50)
    cv2.moveWindow('H - Hue', 650, 50)
    cv2.moveWindow('S - Saturation', 50, 500)
    cv2.moveWindow('V - Value', 650, 500)
    
    # Отображение
    cv2.imshow('Original', img_bgr)
    cv2.imshow('H - Hue', h)
    cv2.imshow('S - Saturation', s)
    cv2.imshow('V - Value', v)
    
    print("\nОкна отображены. Нажмите любую клавишу...")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def create_hsv_visualization():
    """
    Создание визуализации HSV цветового пространства
    """
    print("\n" + "=" * 60)
    print("ВИЗУАЛИЗАЦИЯ: HSV цветовое пространство")
    print("=" * 60)
    
    # Создание спектра HSV
    width = 360
    height = 256
    
    hsv_spectrum = np.zeros((height, width, 3), dtype=np.uint8)
    
    for x in range(width):
        for y in range(height):
            h = int(x * 179 / width)
            s = 255
            v = 255 - int(y * 255 / height)
            
            hsv_spectrum[y, x] = [h, s, v]
    
    # Конвертация в BGR
    bgr_spectrum = cv2.cvtColor(hsv_spectrum, cv2.COLOR_HSV2BGR)
    
    # Добавление подписей
    labeled = bgr_spectrum.copy()
    
    cv2.putText(labeled, "HSV Color Space", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(labeled, "Hue ->", (10, height - 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(labeled, "Value", (10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Отображение
    cv2.namedWindow('HSV Color Space', cv2.WINDOW_NORMAL)
    cv2.imshow('HSV Color Space', labeled)
    
    # Сохранение
    output_path = "output/hsv_spectrum.png"
    cv2.imwrite(output_path, labeled)
    
    print(f"\nЦветовой спектр HSV создан")
    print(f"   Ось X: Hue (0-179)")
    print(f"   Ось Y: Value (255-0)")
    print(f"   Saturation: 255 (константа)")
    print(f"\nСохранено: {output_path}")
    print("\nНажмите любую клавишу...")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    """
    Главная функция
    """
    print("\n" + "=" * 60)
    print(" ЛАБОРАТОРНАЯ РАБОТА №1 - ЗАДАНИЕ 5")
    print(" Формат изображения HSV")
    print("=" * 60)
    
    try:
        # Теория
        explain_hsv()
        
        input("\nНажмите Enter для начала...")
        
        # Основное задание
        show_image_bgr_and_hsv()
        
        input("\nНажмите Enter для просмотра каналов...")
        
        # Раздельные каналы
        show_hsv_channels_separately()
        
        input("\nНажмите Enter для визуализации...")
        
        # Визуализация
        create_hsv_visualization()
        
        print("\n" + "=" * 60)
        print("ЗАДАНИЕ 5 ЗАВЕРШЕНО")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nОшибка: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
