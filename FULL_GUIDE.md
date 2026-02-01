# Лабораторная работа №1 - Компьютерное зрение
## Полный разбор кода и теории

---

## Задание 1: Установка OpenCV

### Команды установки

```bash
# Создание виртуального окружения
python -m venv venv

# Активация (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Установка OpenCV
pip install opencv-python

# Сохранение зависимостей
pip freeze > requirements.txt
```

### Проверка установки

```python
import cv2
print(cv2.__version__)  # Вывод версии OpenCV
```

### Ключевые моменты

- OpenCV в Python называется `cv2`
- Работает с изображениями как с NumPy массивами
- Размер массива: (высота, ширина, каналы)

---

## Задание 2: Вывод изображений

### Основные функции

#### cv2.imread() - загрузка изображения

```python
img = cv2.imread('image.png', cv2.IMREAD_COLOR)
```

**Флаги:**
- `IMREAD_COLOR` (1) — цветное BGR, 3 канала
- `IMREAD_GRAYSCALE` (0) — чёрно-белое, 1 канал
- `IMREAD_UNCHANGED` (-1) — с альфа-каналом

#### cv2.namedWindow() - создание окна

```python
cv2.namedWindow('Window Name', cv2.WINDOW_NORMAL)
```

**Флаги:**
- `WINDOW_NORMAL` — можно менять размер
- `WINDOW_AUTOSIZE` — автоматический размер
- `WINDOW_FULLSCREEN` — полный экран

#### cv2.imshow() - отображение

```python
cv2.imshow('Window Name', image)
```

#### cv2.waitKey() - ожидание клавиши

```python
key = cv2.waitKey(0)  # 0 = ждать бесконечно, код клавиши в key
```

#### cv2.destroyAllWindows() - закрытие окон

```python
cv2.destroyAllWindows()
```

### Типичный код

```python
import cv2

img = cv2.imread('image.png', cv2.IMREAD_COLOR)
cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
cv2.imshow('Display', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Формат изображения в OpenCV

- OpenCV использует **BGR** вместо RGB (Blue-Green-Red)
- Изображение = 3D массив NumPy: [высота, ширина, каналы]
- Тип данных: uint8 (значения 0-255)

---

## Задание 3: Работа с видео

### Класс VideoCapture

#### Открытие видео

```python
# Из файла
cap = cv2.VideoCapture('video.mp4')

# С веб-камеры (0 = первая камера)
cap = cv2.VideoCapture(0)

# Проверка открытия
if not cap.isOpened():
    print("Ошибка: видео не открыто!")
```

#### Чтение кадра

```python
ret, frame = cap.read()
# ret - булево (True если успешно)
# frame - массив с изображением кадра
```

#### Получение свойств (GET)

```python
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
```

#### Установка свойств (SET)

```python
cap.set(cv2.CAP_PROP_POS_FRAMES, 100)   # Перейти к кадру 100
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Установить ширину
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # Установить высоту
```

#### Типичный цикл воспроизведения

```python
while True:
    ret, frame = cap.read()
    
    if not ret:
        break  # Видео закончилось
    
    cv2.imshow('Video', frame)
    
    # Выход по ESC (код 27)
    if cv2.waitKey(25) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
```

#### Конвертация цветовых пространств

```python
# BGR в чёрно-белое
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# BGR в HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# BGR в LAB
lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
```

#### Изменение размера

```python
# Масштабирование кадра
resized = cv2.resize(frame, (640, 480))

# Пропорциональное изменение
scale = 0.5
resized = cv2.resize(frame, 
    (int(width * scale), int(height * scale)))
```

---

## Задание 4: Запись видео в файл

### FourCC - кодек

FourCC (Four Character Code) — 4-символьный код кодека для сжатия видео.

```python
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # XVID для .avi
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4V для .mp4
```

**Популярные кодеки:**
- **XVID** — хорошее сжатие, .avi
- **MJPG** — большой размер, хорошая совместимость, .avi
- **mp4v** — стандартный MPEG-4, .mp4
- **avc1** — H.264, .mp4 (рекомендуется для Windows)

### Создание VideoWriter

```python
out = cv2.VideoWriter(
    'output.avi',       # Имя выходного файла
    fourcc,             # Кодек
    20.0,               # Частота кадров (FPS)
    (640, 480),         # Размер кадра (ширина, высота)
    isColor=True        # Цветное (True) или ч/б (False)
)

# Проверка успешного создания
if not out.isOpened():
    print("Ошибка: не удалось создать VideoWriter!")
```

### Запись кадра

```python
out.write(frame)  # Кадр должен быть того же размера!
```

### Завершение записи

```python
out.release()  # ВАЖНО: без этого файл может быть повреждён!
```

### Типичный процесс копирования видео

```python
# Открываем входное видео
cap = cv2.VideoCapture('input.mp4')
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Создаём VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, fps, (w, h))

# Копируем кадры
while True:
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)

# Освобождаем ресурсы
cap.release()
out.release()
```

### Запись с эффектами

```python
# Чёрно-белое видео
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
out.write(gray_frame)  # Нужно isColor=False в конструкторе

# Уменьшенное видео
resized = cv2.resize(frame, (320, 240))
out.write(resized)

# Отражённое видео
flipped = cv2.flip(frame, 1)  # 1 = горизонтальное отражение
out.write(flipped)
```

---

## Задание 5: Формат HSV

### Что такое HSV?

HSV (Hue, Saturation, Value) — цветовая модель, альтернатива RGB/BGR.

**H (Hue) — Оттенок**
- Диапазон: 0-179 (в теории 0-360°)
- Определяет цвет: красный, зелёный, синий
- Примеры: 0° = красный, 60° = жёлтый, 120° = зелёный

**S (Saturation) — Насыщенность**
- Диапазон: 0-255
- 0 = серый цвет (ненасыщенный)
- 255 = максимально насыщенный, яркий цвет

**V (Value) — Яркость**
- Диапазон: 0-255
- 0 = чёрный цвет
- 255 = максимально яркий цвет

### Преимущества HSV

1. **Выделение цвета** — легче найти объекты определённого цвета
2. **Устойчивость к освещению** — при изменении света меняется только V
3. **Интуитивность** — более естественная модель для человека

### Конвертация между форматами

```python
# BGR в HSV
hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

# HSV в BGR
bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

# HSV в RGB
rgb_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
```

### Работа с отдельными каналами

```python
# Разделение на каналы
h, s, v = cv2.split(hsv_image)

# h, s, v теперь отдельные 2D массивы (одноканальные)
# Можно работать с каждым отдельно

# Слияние каналов обратно
hsv_image = cv2.merge([h, s, v])
```

### Почему HSV выглядит странно?

При `cv2.imshow(hsv_image)` OpenCV показывает:
- Красный канал дисплея = H (оттенок)
- Зелёный канал дисплея = S (насыщенность)
- Синий канал дисплея = V (яркость)

Решение:

```python
# Вариант 1: конвертировать обратно в BGR перед показом
bgr = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
cv2.imshow('HSV', bgr)

# Вариант 2: показывать каналы отдельно
h, s, v = cv2.split(hsv_image)
cv2.imshow('Hue', h)
cv2.imshow('Saturation', s)
cv2.imshow('Value', v)
```

---

## Задание 6: Красный крест с веб-камеры

### Рисование прямоугольника

```python
cv2.rectangle(
    image,              # Изображение для рисования
    (x1, y1),          # Верхний левый угол
    (x2, y2),          # Нижний правый угол
    (B, G, R),         # Цвет в BGR
    thickness          # Толщина линии (или -1 для заливки)
)
```

### Рисование круга

```python
cv2.circle(
    image,              # Изображение
    (cx, cy),          # Центр круга
    radius,            # Радиус
    (B, G, R),         # Цвет
    thickness          # Толщина (-1 = заливка)
)
```

### Цвета в BGR формате

```python
red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (0, 255, 255)
cyan = (255, 255, 0)
magenta = (255, 0, 255)
```

### Вычисление центра изображения

```python
height, width = frame.shape[:2]
center_x = width // 2
center_y = height // 2
```

### Как нарисовать крест

Крест состоит из двух прямоугольников: вертикального и горизонтального.

```python
# Параметры креста
cross_color = (0, 0, 255)  # Красный в BGR
thickness = 3

# Вертикальная часть (узкая, высокая)
cv2.rectangle(frame,
    (center_x - 30, center_y - 90),   # Верхний левый
    (center_x + 30, center_y + 90),   # Нижний правый
    cross_color, thickness)

# Горизонтальная часть (широкая, низкая)
cv2.rectangle(frame,
    (center_x - 90, center_y - 30),   # Верхний левый
    (center_x + 90, center_y + 30),   # Нижний правый
    cross_color, thickness)
```

### Добавление текста

```python
cv2.putText(
    image,                      # Изображение
    "Text",                     # Текст для вывода
    (x, y),                     # Позиция (нижний левый угол)
    cv2.FONT_HERSHEY_SIMPLEX,  # Шрифт
    0.7,                        # Размер шрифта
    (B, G, R),                 # Цвет
    2                           # Толщина линии
)
```

---

## Задание 7: Запись видео с веб-камеры

### Комбинация VideoCapture + VideoWriter

Задание 7 объединяет знания из заданий 3, 4 и 6.

```python
import cv2
from datetime import datetime

# Открываем веб-камеру
cap = cv2.VideoCapture(0)

# Получаем параметры
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 20.0

# Генерируем имя файла с датой
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"output/webcam_{timestamp}.avi"

# Создаём VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_filename, fourcc, fps, 
                      (width, height))

recording = False
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Если идёт запись
    if recording:
        out.write(frame)
        frame_count += 1
        # Красный кружок REC
        cv2.circle(frame, (30, 30), 15, (0, 0, 255), -1)
    
    cv2.imshow('Webcam', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key == ord('r'):  # R
        recording = not recording

cap.release()
out.release()
cv2.destroyAllWindows()
```

### Обработка клавиш

```python
key = cv2.waitKey(1) & 0xFF

# Основные коды
if key == 27:           # ESC - выход
    break
elif key == ord('r'):   # R - toggle запись
    recording = not recording
elif key == 32:         # SPACE - снимок
    cv2.imwrite(f'snapshot_{frame_count}.png', frame)
elif key == ord('q'):   # Q - выход
    break
```

### Маска 0xFF

Маска `0xFF` берёт только младшие 8 бит значения. Это нужно для совместимости с 64-битными системами.

```python
# Правильно
key = cv2.waitKey(1) & 0xFF

# Может не работать на некоторых системах
key = cv2.waitKey(1)
```

### Индикатор записи

```python
# Красный круг в левом верхнем углу
cv2.circle(frame, (30, 30), 15, (0, 0, 255), -1)

# С текстом "REC"
cv2.putText(frame, "REC", (50, 40),
           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# Счётчик кадров
cv2.putText(frame, f"Frames: {frame_count}", (50, 70),
           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
```

---

## Часто задаваемые вопросы

### Q1: Почему OpenCV использует BGR, а не RGB?
**A:** OpenCV разрабатывался изначально для работы с камерами, которые выдавали формат BGR. Это историческое решение, которое осталось в стандарте.

### Q2: Что делает маска & 0xFF в waitKey()?
**A:** Она берёт только младшие 8 бит значения. На 64-битных системах waitKey() может вернуть 32-битное значение, где код клавиши находится в младших 8 битах.

### Q3: Почему видео файл повреждается?
**A:** Если забыть вызвать `out.release()`, файл остаётся открытым и не записывается полностью. Всегда вызывайте `release()` в конце!

### Q4: Почему камера не открывается?
**A:** Возможные причины:
- Камера используется другим приложением
- Нет прав доступа к камере
- Индекс камеры неправильный (попробуйте 1, 2 вместо 0)

### Q5: Что такое fourcc?
**A:** FourCC (Four Character Code) — это 4-символьный код, обозначающий кодек сжатия видео. Примеры: XVID, MJPG, mp4v.

### Q6: Почему H в HSV от 0 до 179, а не 360?
**A:** Экономия памяти. H хранится в uint8 (0-255), но используется только 0-179, чтобы покрыть весь цветовой круг 0-360°.

### Q7: Как выделить объект определённого цвета?
**A:** Конвертируйте в HSV и используйте cv2.inRange():

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Красный цвет: H от 0 до 10 или 170 до 180
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])
mask = cv2.inRange(hsv, lower_red, upper_red)
```

---

## Типичные ошибки и решения

### Ошибка: Assertion failure: size.width>0 && size.height>0

**Причина:** Изображение не загрузилось.

```python
# Неправильно
img = cv2.imread('image.png')
cv2.imshow('img', img)  # Может быть None!

# Правильно
img = cv2.imread('image.png')
if img is None:
    print("Ошибка: файл не загружен")
else:
    cv2.imshow('img', img)
```

### Ошибка: FFMPEG: tag is not supported

**Причина:** Кодек не поддерживается.
**Решение:** Используйте поддерживаемые кодеки (XVID для .avi, mp4v для .mp4).

### Ошибка: VideoWriter не создаёт файл

**Причина:** Забыли вызвать `release()`.

```python
# Неправильно
out = cv2.VideoWriter(...)
out.write(frame)
# Файл будет пуст!

# Правильно
out = cv2.VideoWriter(...)
out.write(frame)
out.release()  # Обязательно!
```

### Ошибка: Камера не открывается

```python
# Решение: проверить возвращаемое значение
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Ошибка: не удалось открыть камеру")
    # Попробуйте другой индекс (1, 2, ...)
    cap = cv2.VideoCapture(1)
```

### Ошибка: Размер кадра не совпадает

**Причина:** VideoWriter требует кадры определённого размера.

```python
# Правильно: указываем размер и проверяем
width = 640
height = 480
out = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if frame.shape[1] != width or frame.shape[0] != height:
        frame = cv2.resize(frame, (width, height))
    out.write(frame)
```

---

## Полезные константы и коды

### Коды клавиш

```python
key = cv2.waitKey(1) & 0xFF

# Основные коды
if key == 27:           # ESC
    break
elif key == 32:         # SPACE
    pass
elif key == 13:         # ENTER
    pass
elif key == ord('r'):   # Буква R
    pass
elif key == ord('q'):   # Буква Q
    pass
```

### Свойства VideoCapture

```python
cv2.CAP_PROP_FRAME_WIDTH        # Ширина кадра
cv2.CAP_PROP_FRAME_HEIGHT       # Высота кадра
cv2.CAP_PROP_FPS                # Частота кадров
cv2.CAP_PROP_FRAME_COUNT        # Количество кадров
cv2.CAP_PROP_POS_FRAMES         # Текущая позиция (кадр)
cv2.CAP_PROP_BRIGHTNESS         # Яркость
cv2.CAP_PROP_CONTRAST           # Контраст
cv2.CAP_PROP_SATURATION         # Насыщенность
```

### Основные цвета в BGR

```python
# (Blue, Green, Red)
red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)
yellow = (0, 255, 255)
cyan = (255, 255, 0)
magenta = (255, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
```

### Преобразования цветов

```python
cv2.COLOR_BGR2GRAY          # BGR -> Grayscale
cv2.COLOR_BGR2HSV           # BGR -> HSV
cv2.COLOR_BGR2LAB           # BGR -> LAB
cv2.COLOR_BGR2YCrCb         # BGR -> YCrCb
cv2.COLOR_BGR2RGB           # BGR -> RGB
cv2.COLOR_HSV2BGR           # HSV -> BGR
```

## Заключение

В этой лабораторной работе были изучены основные функции библиотеки OpenCV:

- **Загрузка и отображение изображений** — cv2.imread(), imshow(), waitKey()
- **Работа с видео** — VideoCapture класс для захвата видео
- **Запись видео** — VideoWriter класс с различными кодеками
- **Цветовые преобразования** — BGR, HSV и другие форматы
- **Рисование фигур** — rectangle(), circle(), putText()
- **Реальные приложения** — захват с веб-камеры и запись видео

Все полученные навыки являются фундаментом для дальнейшего изучения компьютерного зрения и применения OpenCV в реальных проектах.
