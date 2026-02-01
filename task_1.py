import cv2
import sys

def test_opencv():
    """Проверка установки OpenCV"""
    print(f"OpenCV версия: {cv2.__version__}")
    print(f"Python версия: {sys.version}")
    print("OpenCV успешно установлен! ✓")

if __name__ == "__main__":
    test_opencv()
