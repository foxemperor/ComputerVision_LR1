import cv2
import os


def display_video_info(cap):
    """
    Вывод информации о видео
    """
    # Получаем свойства видео через методы get()
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"\n📹 Информация о видео:")
    print(f"   • Разрешение: {width}x{height}")
    print(f"   • FPS (кадров/сек): {fps:.2f}")
    print(f"   • Всего кадров: {frame_count}")
    print(f"   • Длительность: {frame_count/fps:.2f} секунд")
    print(f"   • Backend: {cap.getBackendName()}")
    
    return width, height, fps, frame_count


def play_video_original():
    """
    Задание 3.1: Воспроизведение видео в оригинальном виде
    """
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 3.1: Воспроизведение оригинального видео")
    print("=" * 60)
    
    video_path = "videos/test_video.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Ошибка: файл {video_path} не найден!")
        print("Поместите тестовое видео в папку 'videos/'")
        return
    
    # Открываем видеопоток
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("❌ Не удалось открыть видео!")
        return
    
    # Выводим информацию о видео
    display_video_info(cap)
    
    print("\n▶️  Воспроизведение... (Нажмите ESC для выхода)")
    
    # Создаем окно
    window_name = "Original Video"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    # Воспроизведение
    while True:
        ret, frame = cap.read()
        
        # Если кадры закончились, начинаем заново
        if not ret:
            print("🔄 Видео закончилось, перезапуск...")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        
        # Отображаем кадр
        cv2.imshow(window_name, frame)
        
        # Выход по клавише ESC (код 27)
        if cv2.waitKey(25) & 0xFF == 27:
            break
    
    cap.release()
    cv2.destroyWindow(window_name)
    print("✅ Воспроизведение завершено\n")


def play_video_resized():
    """
    Задание 3.2: Воспроизведение с изменением размера
    """
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 3.2: Изменение размера видео")
    print("=" * 60)
    
    video_path = "videos/test_video.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Ошибка: файл {video_path} не найден!")
        return
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("❌ Не удалось открыть видео!")
        return
    
    width, height, fps, _ = display_video_info(cap)
    
    # Варианты масштабирования
    scales = [
        (0.5, "50% размера"),
        (1.5, "150% размера"),
        (2.0, "200% размера")
    ]
    
    for scale, description in scales:
        print(f"\n🔍 Масштаб: {description}")
        
        new_width = int(width * scale)
        new_height = int(height * scale)
        print(f"   Новое разрешение: {new_width}x{new_height}")
        
        window_name = f"Resized Video - {description}"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        
        # Сбрасываем позицию в начало
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        frame_counter = 0
        max_frames = 90  # Показываем по 90 кадров для каждого масштаба
        
        print(f"   ▶️  Воспроизведение... (Нажмите ESC для пропуска)")
        
        while frame_counter < max_frames:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Изменяем размер кадра
            resized_frame = cv2.resize(frame, (new_width, new_height))
            
            cv2.imshow(window_name, resized_frame)
            
            if cv2.waitKey(25) & 0xFF == 27:
                break
            
            frame_counter += 1
        
        cv2.destroyWindow(window_name)
    
    cap.release()
    print("\n✅ Тест масштабирования завершен\n")


def play_video_color_modes():
    """
    Задание 3.3: Различные цветовые форматы
    """
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 3.3: Цветовые форматы видео")
    print("=" * 60)
    
    video_path = "videos/test_video.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Ошибка: файл {video_path} не найден!")
        return
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("❌ Не удалось открыть видео!")
        return
    
    display_video_info(cap)
    
    # Цветовые режимы
    color_modes = [
        ("BGR (оригинал)", None),
        ("Grayscale (оттенки серого)", cv2.COLOR_BGR2GRAY),
        ("HSV", cv2.COLOR_BGR2HSV),
        ("LAB", cv2.COLOR_BGR2LAB),
        ("YCrCb", cv2.COLOR_BGR2YCrCb)
    ]
    
    for mode_name, conversion in color_modes:
        print(f"\n🎨 Режим: {mode_name}")
        
        window_name = f"Color Mode: {mode_name}"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        
        # Сбрасываем позицию в начало
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        frame_counter = 0
        max_frames = 90
        
        print(f"   ▶️  Воспроизведение... (Нажмите ESC для пропуска)")
        
        while frame_counter < max_frames:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Конвертируем цветовое пространство
            if conversion is not None:
                converted_frame = cv2.cvtColor(frame, conversion)
            else:
                converted_frame = frame
            
            cv2.imshow(window_name, converted_frame)
            
            if cv2.waitKey(25) & 0xFF == 27:
                break
            
            frame_counter += 1
        
        cv2.destroyWindow(window_name)
    
    cap.release()
    print("\n✅ Тест цветовых форматов завершен\n")


def test_videocapture_methods():
    """
    Задание 3.4: Тестирование методов класса VideoCapture
    """
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 3.4: Методы класса VideoCapture")
    print("=" * 60)
    
    video_path = "videos/test_video.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Ошибка: файл {video_path} не найден!")
        return
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("❌ Не удалось открыть видео!")
        return
    
    print("\n📋 Тестирование GET методов:")
    print("-" * 60)
    
    # Основные свойства
    properties = {
        "CAP_PROP_FRAME_WIDTH": cv2.CAP_PROP_FRAME_WIDTH,
        "CAP_PROP_FRAME_HEIGHT": cv2.CAP_PROP_FRAME_HEIGHT,
        "CAP_PROP_FPS": cv2.CAP_PROP_FPS,
        "CAP_PROP_FRAME_COUNT": cv2.CAP_PROP_FRAME_COUNT,
        "CAP_PROP_BRIGHTNESS": cv2.CAP_PROP_BRIGHTNESS,
        "CAP_PROP_CONTRAST": cv2.CAP_PROP_CONTRAST,
        "CAP_PROP_SATURATION": cv2.CAP_PROP_SATURATION,
        "CAP_PROP_HUE": cv2.CAP_PROP_HUE,
    }
    
    for prop_name, prop_id in properties.items():
        value = cap.get(prop_id)
        print(f"   {prop_name:30} = {value}")
    
    # Тестирование SET методов
    print("\n📝 Тестирование SET методов:")
    print("-" * 60)
    
    # Переход к середине видео
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    middle_frame = frame_count // 2
    
    print(f"\n   Переход к кадру {middle_frame} (середина видео)...")
    cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
    
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Middle Frame", frame)
        print(f"   ✓ Текущая позиция: кадр {int(cap.get(cv2.CAP_PROP_POS_FRAMES))}")
        print("   Нажмите любую клавишу...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    # Возврат в начало
    print("\n   Возврат в начало видео...")
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    print(f"   ✓ Текущая позиция: кадр {int(cap.get(cv2.CAP_PROP_POS_FRAMES))}")
    
    cap.release()
    print("\n✅ Тест методов завершен\n")


def main():
    """
    Главная функция
    """
    print("\n" + "=" * 60)
    print(" ЛАБОРАТОРНАЯ РАБОТА №1 - ЗАДАНИЕ 3")
    print(" Работа с видео в OpenCV")
    print("=" * 60)
    
    try:
        # Запускаем все тесты
        play_video_original()
        
        input("Нажмите Enter для продолжения (тест масштабирования)...")
        play_video_resized()
        
        input("Нажмите Enter для продолжения (тест цветов)...")
        play_video_color_modes()
        
        input("Нажмите Enter для продолжения (тест методов)...")
        test_videocapture_methods()
        
        print("\n" + "=" * 60)
        print("🎉 ВСЕ ТЕСТЫ ЗАДАНИЯ 3 УСПЕШНО ЗАВЕРШЕНЫ!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
