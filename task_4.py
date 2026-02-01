import cv2
import os


def copy_video_basic():
    """
    Задание 4.1: Простое копирование видео
    """
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 4.1: Простое копирование видео")
    print("=" * 60)
    
    input_path = "videos/test_video.mp4"
    output_path = "output/copied_video.avi"
    
    # Проверка существования входного файла
    if not os.path.exists(input_path):
        print(f"❌ Ошибка: файл {input_path} не найден!")
        return
    
    # Создаём папку output, если её нет
    os.makedirs("output", exist_ok=True)
    
    # Открываем входное видео
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print("❌ Не удалось открыть видео!")
        return
    
    # Получаем параметры видео
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"\n📹 Исходное видео:")
    print(f"   • Разрешение: {width}x{height}")
    print(f"   • FPS: {fps:.2f}")
    print(f"   • Кадров: {frame_count}")
    
    # Создаём VideoWriter
    # fourcc - 4-символьный код кодека
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # XVID кодек для .avi
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    if not out.isOpened():
        print("❌ Не удалось создать выходное видео!")
        cap.release()
        return
    
    print(f"\n📝 Начинаем копирование...")
    print(f"   Выходной файл: {output_path}")
    
    frame_num = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Записываем кадр
        out.write(frame)
        
        frame_num += 1
        
        # Показываем прогресс
        if frame_num % 30 == 0:
            progress = (frame_num / frame_count) * 100
            print(f"   Прогресс: {frame_num}/{frame_count} ({progress:.1f}%)")
    
    # Освобождаем ресурсы
    cap.release()
    out.release()
    
    # Проверяем размер файла
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # МБ
        print(f"\n✅ Копирование завершено!")
        print(f"   Записано кадров: {frame_num}")
        print(f"   Размер файла: {file_size:.2f} МБ")
    else:
        print("❌ Выходной файл не создан!")


def copy_video_with_codec_tests():
    """
    Задание 4.2: Копирование с разными кодеками
    """
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 4.2: Тестирование разных кодеков")
    print("=" * 60)
    
    input_path = "videos/test_video.mp4"
    
    if not os.path.exists(input_path):
        print(f"❌ Ошибка: файл {input_path} не найден!")
        return
    
    # Открываем входное видео
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print("❌ Не удалось открыть видео!")
        return
    
    # Параметры видео
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Разные кодеки для тестирования
    # Используем только надёжные кодеки для Windows
    codecs = [
        ('XVID', 'avi', "XVID - DivX MPEG-4 (рекомендуется)"),
        ('MJPG', 'avi', "MJPEG - Motion JPEG (большой размер)"),
        ('mp4v', 'mp4', "MP4V - MPEG-4 (стандартный)"),
        ('avc1', 'mp4', "AVC1 - H.264 (совместимый вариант)"),
    ]
    
    print("\n💡 Примечание: X264 заменён на AVC1 для совместимости с Windows")
    
    for codec_name, extension, description in codecs:
        print(f"\n🎬 Кодек: {description}")
        
        output_path = f"output/video_{codec_name}.{extension}"
        
        # Сбрасываем позицию в начало
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        try:
            # Создаём fourcc
            fourcc = cv2.VideoWriter_fourcc(*codec_name)
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            if not out.isOpened():
                print(f"   ⚠️  Не удалось инициализировать кодек {codec_name}")
                continue
            
            # Записываем только первые 90 кадров для экономии времени
            max_frames = min(90, frame_count)
            
            written_frames = 0
            for i in range(max_frames):
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
                written_frames += 1
            
            out.release()
            
            # Проверяем результат
            if os.path.exists(output_path) and written_frames > 0:
                file_size = os.path.getsize(output_path) / 1024  # КБ
                print(f"   ✓ Файл: {output_path}")
                print(f"   ✓ Кадров: {written_frames}")
                print(f"   ✓ Размер: {file_size:.2f} КБ")
            else:
                print(f"   ❌ Файл не создан или пуст!")
                
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    cap.release()
    print("\n✅ Тест кодеков завершен")


def copy_video_with_effects():
    """
    Задание 4.3: Копирование с применением эффектов
    """
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 4.3: Копирование с эффектами")
    print("=" * 60)
    
    input_path = "videos/test_video.mp4"
    
    if not os.path.exists(input_path):
        print(f"❌ Ошибка: файл {input_path} не найден!")
        return
    
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print("❌ Не удалось открыть видео!")
        return
    
    # Параметры
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Эффекты
    effects = [
        ("grayscale", "Черно-белое видео"),
        ("resized", "Уменьшенное 50%"),
        ("flipped", "Отражённое по горизонтали"),
    ]
    
    for effect_name, description in effects:
        print(f"\n🎨 Эффект: {description}")
        
        output_path = f"output/video_{effect_name}.avi"
        
        # Сброс позиции
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        # Определяем размер для записи в зависимости от эффекта
        if effect_name == "resized":
            out_width = width // 2
            out_height = height // 2
        else:
            out_width = width
            out_height = height
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        
        # Для grayscale нужно указать isColor=False
        if effect_name == "grayscale":
            out = cv2.VideoWriter(output_path, fourcc, fps, 
                                (out_width, out_height), isColor=False)
        else:
            out = cv2.VideoWriter(output_path, fourcc, fps, 
                                (out_width, out_height))
        
        if not out.isOpened():
            print(f"   ❌ Не удалось создать выходной файл!")
            continue
        
        frame_count = 0
        max_frames = 90  # Ограничиваем для скорости
        
        while frame_count < max_frames:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Применяем эффект
            if effect_name == "grayscale":
                processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elif effect_name == "resized":
                processed_frame = cv2.resize(frame, (out_width, out_height))
            elif effect_name == "flipped":
                processed_frame = cv2.flip(frame, 1)  # 1 = horizontal flip
            else:
                processed_frame = frame
            
            out.write(processed_frame)
            frame_count += 1
        
        out.release()
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / 1024
            print(f"   ✓ Файл: {output_path}")
            print(f"   ✓ Кадров: {frame_count}")
            print(f"   ✓ Размер: {file_size:.2f} КБ")
    
    cap.release()
    print("\n✅ Копирование с эффектами завершено")


def compare_original_and_copy():
    """
    Задание 4.4: Сравнение оригинала и копии
    """
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 4.4: Воспроизведение оригинала и копии")
    print("=" * 60)
    
    original_path = "videos/test_video.mp4"
    copy_path = "output/copied_video.avi"
    
    if not os.path.exists(original_path):
        print(f"❌ Оригинал не найден: {original_path}")
        return
    
    if not os.path.exists(copy_path):
        print(f"❌ Копия не найдена: {copy_path}")
        print("   Сначала выполните задание 4.1")
        return
    
    cap_orig = cv2.VideoCapture(original_path)
    cap_copy = cv2.VideoCapture(copy_path)
    
    if not cap_orig.isOpened() or not cap_copy.isOpened():
        print("❌ Не удалось открыть видео!")
        return
    
    print("\n📊 Сравнение файлов:")
    print(f"   Оригинал: {os.path.getsize(original_path) / (1024*1024):.2f} МБ")
    print(f"   Копия: {os.path.getsize(copy_path) / (1024*1024):.2f} МБ")
    
    print("\n▶️  Воспроизведение (ESC для выхода)...")
    
    cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Copy", cv2.WINDOW_NORMAL)
    
    # Располагаем окна рядом
    cv2.moveWindow("Original", 100, 100)
    cv2.moveWindow("Copy", 750, 100)
    
    frame_num = 0
    
    while True:
        ret_orig, frame_orig = cap_orig.read()
        ret_copy, frame_copy = cap_copy.read()
        
        if not ret_orig or not ret_copy:
            print("   Видео закончилось")
            break
        
        cv2.imshow("Original", frame_orig)
        cv2.imshow("Copy", frame_copy)
        
        frame_num += 1
        
        if cv2.waitKey(25) & 0xFF == 27:  # ESC
            break
    
    cap_orig.release()
    cap_copy.release()
    cv2.destroyAllWindows()
    
    print(f"✅ Воспроизведено кадров: {frame_num}")


def main():
    """
    Главная функция
    """
    print("\n" + "=" * 60)
    print(" ЛАБОРАТОРНАЯ РАБОТА №1 - ЗАДАНИЕ 4")
    print(" Запись видео из файла в другой файл")
    print("=" * 60)
    
    try:
        # Задание 4.1 - Простое копирование
        copy_video_basic()
        
        input("\nНажмите Enter для продолжения (тест кодеков)...")
        
        # Задание 4.2 - Разные кодеки
        copy_video_with_codec_tests()
        
        input("\nНажмите Enter для продолжения (эффекты)...")
        
        # Задание 4.3 - С эффектами
        copy_video_with_effects()
        
        input("\nНажмите Enter для продолжения (сравнение)...")
        
        # Задание 4.4 - Сравнение
        compare_original_and_copy()
        
        print("\n" + "=" * 60)
        print("🎉 ВСЕ ТЕСТЫ ЗАДАНИЯ 4 УСПЕШНО ЗАВЕРШЕНЫ!")
        print("=" * 60)
        print(f"\n📁 Все видео сохранены в папке: output/")
        
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
