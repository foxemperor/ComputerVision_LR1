import cv2
import os
from datetime import datetime


def record_video_from_camera():
    """
    Задание 7: Захват видео с веб-камеры и запись в файл
    """
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 7: Запись видео с веб-камеры")
    print("=" * 60)
    
    # Открываем веб-камеру
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Ошибка: не удалось открыть камеру")
        return None
    
    # Устанавливаем параметры
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Получаем параметры видео
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 20.0  # Устанавливаем FPS вручную для стабильности
    
    print(f"\nПараметры камеры:")
    print(f"   Разрешение: {width}x{height}")
    print(f"   FPS: {fps}")
    
    # Создаём папку output
    os.makedirs("output", exist_ok=True)
    
    # Генерируем имя файла с датой и временем
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"output/webcam_recording_{timestamp}.avi"
    
    # Создаём VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))
    
    if not out.isOpened():
        print("Ошибка: не удалось создать VideoWriter")
        cap.release()
        return None
    
    print(f"\nФайл для записи: {output_filename}")
    print("\nУправление:")
    print("   R - начать/остановить запись")
    print("   ESC - выход")
    print("\nОжидание команды...")
    
    cv2.namedWindow('Webcam Recording', cv2.WINDOW_NORMAL)
    
    recording = False
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Ошибка: не удалось захватить кадр")
            break
        
        # Создаём копию для отображения
        display_frame = frame.copy()
        
        # Если идёт запись
        if recording:
            out.write(frame)
            frame_count += 1
            
            # Индикатор записи (красный кружок)
            cv2.circle(display_frame, (30, 30), 15, (0, 0, 255), -1)
            cv2.putText(
                display_frame,
                f"REC | Frames: {frame_count}",
                (60, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )
        else:
            # Текст "Готов к записи"
            cv2.putText(
                display_frame,
                "Press R to start recording",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
        
        # Инструкции
        cv2.putText(
            display_frame,
            "R - record, ESC - exit",
            (10, height - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1
        )
        
        cv2.imshow('Webcam Recording', display_frame)
        
        # Обработка клавиш
        key = cv2.waitKey(1) & 0xFF
        
        if key == 27:  # ESC
            print("\nВыход из программы")
            break
        elif key == ord('r') or key == ord('R'):
            recording = not recording
            if recording:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Запись началась...")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Запись остановлена. Записано кадров: {frame_count}")
    
    # Освобождение ресурсов
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    # Проверяем результат
    if frame_count > 0 and os.path.exists(output_filename):
        file_size = os.path.getsize(output_filename) / (1024 * 1024)
        print(f"\nЗапись завершена:")
        print(f"   Файл: {output_filename}")
        print(f"   Кадров: {frame_count}")
        print(f"   Размер: {file_size:.2f} МБ")
        print(f"   Длительность: {frame_count / fps:.1f} секунд")
        return output_filename
    else:
        print("\nЗапись не производилась или файл пуст")
        if os.path.exists(output_filename):
            os.remove(output_filename)
        return None


def playback_recorded_video(filename):
    """
    Воспроизведение записанного видео
    """
    print("\n" + "=" * 60)
    print("ВОСПРОИЗВЕДЕНИЕ ЗАПИСАННОГО ВИДЕО")
    print("=" * 60)
    
    if filename is None or not os.path.exists(filename):
        print("Ошибка: файл не найден или не был создан")
        return
    
    cap = cv2.VideoCapture(filename)
    
    if not cap.isOpened():
        print("Ошибка: не удалось открыть видео файл")
        return
    
    # Информация о файле
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"\nИнформация о файле:")
    print(f"   Разрешение: {width}x{height}")
    print(f"   FPS: {fps:.2f}")
    print(f"   Кадров: {frame_count}")
    print(f"   Длительность: {frame_count/fps:.1f} секунд")
    print("\nВоспроизведение (ESC - выход)...")
    
    cv2.namedWindow('Playback', cv2.WINDOW_NORMAL)
    
    current_frame = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("\nВидео закончилось, перезапуск...")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            current_frame = 0
            continue
        
        current_frame += 1
        
        # Добавляем счётчик кадров
        cv2.putText(
            frame,
            f"Frame: {current_frame}/{frame_count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
        
        cv2.imshow('Playback', frame)
        
        # Задержка для корректного FPS
        delay = int(1000 / fps) if fps > 0 else 30
        
        if cv2.waitKey(delay) & 0xFF == 27:  # ESC
            print("\nВоспроизведение остановлено")
            break
    
    cap.release()
    cv2.destroyAllWindows()


def main():
    """
    Главная функция
    """
    print("\n" + "=" * 60)
    print(" ЛАБОРАТОРНАЯ РАБОТА №1 - ЗАДАНИЕ 7")
    print(" Запись видео с веб-камеры")
    print("=" * 60)
    
    try:
        # Шаг 1: Запись видео
        recorded_file = record_video_from_camera()
        
        # Шаг 2: Воспроизведение
        if recorded_file:
            input("\nНажмите Enter для воспроизведения записанного видео...")
            playback_recorded_video(recorded_file)
        
        print("\n" + "=" * 60)
        print("ЗАДАНИЕ 7 ЗАВЕРШЕНО")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nОшибка: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
