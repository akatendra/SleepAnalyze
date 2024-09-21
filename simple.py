import cv2

# Инициализация камеры
cap = cv2.VideoCapture(1)  # 0 для встроенной камеры, 1 или другой номер для внешней

# Получение параметров видео
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
print(f'width x height: {width} x {height} fps: {fps}')

# Создание объекта для записи видео
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Not working
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Запись кадра в файл
    out.write(frame)

    # Отображение кадра (опционально)
    cv2.imshow('frame', frame)

    # Выход по нажатию клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
out.release()
cv2.destroyAllWindows()