import cv2
import os


def test_imread_flags():
    """
    Тестирование флагов чтения изображения (imread)
    """
    print("=" * 60)
    print("ТЕСТ 1: Флаги чтения изображения (imread)")
    print("=" * 60)
    
    # Путь к изображению
    image_path = "images/test_image.png"
    
    if not os.path.exists(image_path):
        print(f"❌ Ошибка: файл {image_path} не найден!")
        print("Создайте папку 'images' и добавьте test_image.png")
        return
    
    # Флаги для тестирования
    flags = {
        "IMREAD_COLOR": cv2.IMREAD_COLOR,           # Цветное изображение (BGR)
        "IMREAD_GRAYSCALE": cv2.IMREAD_GRAYSCALE,   # Черно-белое
        "IMREAD_UNCHANGED": cv2.IMREAD_UNCHANGED    # С альфа-каналом
    }
    
    for flag_name, flag_value in flags.items():
        print(f"\n📷 Загрузка с флагом: {flag_name}")
        
        # Загружаем изображение
        img = cv2.imread(image_path, flag_value)
        
        if img is None:
            print(f"   ❌ Ошибка загрузки!")
            continue
        
        # Выводим информацию
        print(f"   ✓ Размер: {img.shape}")
        print(f"   ✓ Тип данных: {img.dtype}")
        
        # Отображаем
        window_name = f"imread: {flag_name}"
        cv2.imshow(window_name, img)
        print(f"   ✓ Нажмите любую клавишу для продолжения...")
        cv2.waitKey(0)
        cv2.destroyWindow(window_name)
    
    print("\n✅ Тест флагов imread завершен\n")


def test_window_flags():
    """
    Тестирование флагов создания окна (namedWindow)
    """
    print("=" * 60)
    print("ТЕСТ 2: Флаги создания окна (namedWindow)")
    print("=" * 60)
    
    image_path = "images/test_image.png"
    
    if not os.path.exists(image_path):
        print(f"❌ Ошибка: файл {image_path} не найден!")
        return
    
    # Загружаем изображение один раз
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    if img is None:
        print(f"❌ Ошибка загрузки изображения!")
        return
    
    # Флаги для окна
    window_flags = {
        "WINDOW_NORMAL": cv2.WINDOW_NORMAL,         # Изменяемый размер
        "WINDOW_AUTOSIZE": cv2.WINDOW_AUTOSIZE,     # Автоматический размер
        "WINDOW_FULLSCREEN": cv2.WINDOW_FULLSCREEN  # Полноэкранный режим
    }
    
    for flag_name, flag_value in window_flags.items():
        print(f"\n🖼️  Окно с флагом: {flag_name}")
        
        window_name = f"Window: {flag_name}"
        
        # Создаем окно с флагом
        cv2.namedWindow(window_name, flag_value)
        
        # Описание флага
        descriptions = {
            "WINDOW_NORMAL": "   → Можно изменять размер мышью",
            "WINDOW_AUTOSIZE": "   → Размер автоматический, изменение запрещено",
            "WINDOW_FULLSCREEN": "   → Полноэкранный режим"
        }
        print(descriptions[flag_name])
        
        # Отображаем изображение
        cv2.imshow(window_name, img)
        print(f"   ✓ Нажмите любую клавишу для продолжения...")
        
        cv2.waitKey(0)
        cv2.destroyWindow(window_name)
    
    print("\n✅ Тест флагов namedWindow завершен\n")


def test_image_formats():
    """
    Тестирование разных форматов изображений
    """
    print("=" * 60)
    print("ТЕСТ 3: Форматы изображений")
    print("=" * 60)
    
    # Форматы для тестирования
    formats = ["png", "jpg", "bmp"]
    
    for fmt in formats:
        image_path = f"images/test_image.{fmt}"
        print(f"\n📁 Загрузка формата: .{fmt.upper()}")
        
        if not os.path.exists(image_path):
            print(f"   ⚠️  Файл {image_path} не найден, пропускаем...")
            continue
        
        # Загружаем
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        
        if img is None:
            print(f"   ❌ Ошибка загрузки!")
            continue
        
        # Информация о файле
        file_size = os.path.getsize(image_path)
        print(f"   ✓ Размер файла: {file_size / 1024:.2f} KB")
        print(f"   ✓ Разрешение: {img.shape[1]}x{img.shape[0]}")
        print(f"   ✓ Каналов: {img.shape[2] if len(img.shape) == 3 else 1}")
        
        # Отображаем
        window_name = f"Format: .{fmt.upper()}"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.imshow(window_name, img)
        print(f"   ✓ Нажмите любую клавишу для продолжения...")
        cv2.waitKey(0)
        cv2.destroyWindow(window_name)
    
    print("\n✅ Тест форматов изображений завершен\n")


def main():
    """
    Главная функция - запуск всех тестов
    """
    print("\n" + "=" * 60)
    print(" ЛАБОРАТОРНАЯ РАБОТА №1 - ЗАДАНИЕ 2")
    print(" Тестирование вывода изображений")
    print("=" * 60 + "\n")
    
    try:
        # Запускаем тесты по порядку
        test_imread_flags()
        test_window_flags()
        test_image_formats()
        
        print("=" * 60)
        print("🎉 ВСЕ ТЕСТЫ УСПЕШНО ЗАВЕРШЕНЫ!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
    
    finally:
        # Закрываем все окна на всякий случай
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
