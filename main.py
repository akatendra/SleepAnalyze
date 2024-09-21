# Camera:
# https://www.aliexpress.com/item/1005005913312412.html?spm=a2g0o.order_list.order_list_main.5.22111802P8H7Lh

# Resolutions:
# '320.0x240.0': 'OK',
# '640.0x480.0': 'OK',
# '800.0x600.0': 'OK',
# '1024.0x768.0': 'OK',
# '1280.0x720.0': 'OK',
# '1280.0x960.0': 'OK',
# '1440.0x1080.0': 'OK',
# '1920.0x1080.0': 'OK'
import cv2
import cv2
import pygame
import time
import datetime
import os


def draw_center_lines(img, cx, cy, color=(0, 0, 0), thickness=1):
    """
    Рисует вертикальную и горизонтальную линии через заданную точку (cx, cy).

    :param img: Исходное изображение
    :param cx: X-координата центральной точки
    :param cy: Y-координата центральной точки
    :param color: Цвет линий (B, G, R)
    :param thickness: Толщина линий
    :return: Изображение с нарисованными линиями
    """
    height, width = img.shape[:2]

    # Рисуем вертикальную линию
    cv2.line(img, (int(cx), 0), (int(cx), height), color, thickness)

    # Рисуем горизонтальную линию
    cv2.line(img, (0, int(cy)), (width, int(cy)), color, thickness)

    return img


def create_video_writer(fps, fourcc, frame_size, duration_hours=1):
    start_time = time.time()
    end_time = start_time + (duration_hours * 3600)  # 3600 секунд в часе

    start_datetime = datetime.datetime.fromtimestamp(start_time)
    end_datetime = datetime.datetime.fromtimestamp(end_time)

    filename = f"recordings/{start_datetime.strftime('%Y-%m-%d_%H-%M-%S')}_to_{end_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.mp4"

    out = cv2.VideoWriter(filename, fourcc, fps, frame_size)
    if not out.isOpened():
        print(f"Ошибка при создании файла {filename}")
        return None, None

    return out, end_time


def add_timestamp(frame, current_time):
    timestamp = datetime.datetime.fromtimestamp(current_time).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    # Настройки текста
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5  # Уменьшаем размер шрифта в 2 раза
    font_color = (0, 0, 0)  # Черный цвет текста
    thickness = 1

    # Получаем размеры текста
    text_size = cv2.getTextSize(timestamp, font, font_scale, thickness)[0]

    # Создаем белый прямоугольник как фон
    padding = 5  # Отступ вокруг текста
    bg_rect = [(10, 10), (10 + text_size[0] + 2 * padding, 10 + text_size[1] + 2 * padding)]
    cv2.rectangle(frame, bg_rect[0], bg_rect[1], (255, 255, 255), -1)

    # Размещаем текст на прямоугольнике
    text_org = (10 + padding, 10 + text_size[1] + padding)
    cv2.putText(frame, timestamp, text_org, font, font_scale, font_color, thickness)

    return frame
#-----------------------------------------------------------------------------------------------------------------------
def main():
    # Инициализация Pygame
    pygame.init()
    clock = pygame.time.Clock()

    prev_time = time.time()
    fps_counter = 0
    real_fps = 10

    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Ошибка при открытии камеры")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # fourcc = cv2.VideoWriter.fourcc('M', 'J', 'P', 'G')


    # fps = 10.0
    # cap.set(cv2.CAP_PROP_FPS, fps)

    cap.set(cv2.CAP_PROP_FOURCC, fourcc)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
    # or
    # width = cap.get(3)  # float `width`
    # height = cap.get(4)  # float `height`

    print(f'Assigned width x height: {frame_width}x{frame_height}')

    fps = cap.get(cv2.CAP_PROP_FPS)
    # or
    # fps = cap.get(5)

    print(f'fps from cap.get(cv2.CAP_PROP_FPS): {fps} (cap.get(5): {cap.get(5)})')  # float `fps`

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # or
    # frame_count = cap.get(7)

    print('frames count:', frame_count)  # float `frame_count`
    # https://stackoverflow.com/questions/63256300/how-do-i-get-usb-webcam-property-ids-for-opencv/63265171#63265171
    # https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
    zoom = cap.get(cv2.CAP_PROP_ZOOM)
    print('zoom:', zoom)
    focus = cap.get(cv2.CAP_PROP_FOCUS)
    print('focus:', focus)
    autofocus = cap.get(cv2.CAP_PROP_AUTOFOCUS)
    print('autofocus:', autofocus)
    print('#################################################################################################################\n\n\n')
    # ============================== OUTPUT VIDEO ==============================
    if not os.path.exists('recordings'):
        os.makedirs('recordings')

    fps_output = 30
    video_output, end_time = create_video_writer(fps_output, fourcc, (frame_width, frame_height))
    # ============================== OUTPUT VIDEO ==============================

    counter = 0
    try:
        while True:
            # Capture the video frame by frame
            ret, frame = cap.read()
            if not ret:
                print("Ошибка при получении кадра")
                break

            counter += 1
            fps_counter += 1

            frame_with_center_lines = draw_center_lines(frame.copy(), frame_width / 2, frame_height / 2)

            # ============================== FPS =======================================
            fps = cap.get(cv2.CAP_PROP_FPS)
            print(f'fps from cap.get(cv2.CAP_PROP_FPS): {fps} (cap.get(5): {cap.get(5)})')

            if time.time() - prev_time >= 1:
                elapsed_time = time.time() - prev_time
                real_fps = fps_counter / elapsed_time
                fps_counter = 0
                prev_time = time.time()

            print(f"Real FPS: {real_fps}")

            clock.tick()  # Счетчик времени для FPS

            # Получение текущего FPS
            pygame_fps = clock.get_fps()
            print(f"PyGame FPS: {pygame_fps:.2f}")
            # ============================== FPS =======================================

            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            print('frames count:', frame_count)  # float `frame_count`
            zoom = cap.get(cv2.CAP_PROP_ZOOM)
            print('zoom:', zoom)
            focus = cap.get(cv2.CAP_PROP_FOCUS)
            print('focus:', focus)
            autofocus = cap.get(cv2.CAP_PROP_AUTOFOCUS)
            print('autofocus:', autofocus)

            current_time = time.time()
            frame = add_timestamp(frame, current_time)
            frame_with_center_lines = add_timestamp(frame_with_center_lines, current_time)

            video_output.write(frame)

            if current_time >= end_time:
                video_output.release()
                video_output, end_time = create_video_writer(fps_output, fourcc,(frame_width, frame_height))

            cv2.imshow('frame', frame_with_center_lines)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # h, w = frame.shape[:2]
            # print(f'w x h = {w} x {h}')
            # print('frame.shape[::-1]: ', frame.shape[::-1])

            key = cv2.waitKey(1)
            if key == ord("q"):
                break
            elif key == ord("s"):
                cv2.imwrite(f'img_{counter}.jpg', frame)

            print(
                '#################################################################################################################\n')
    finally:
        # Release the cap object after the loop
        cap.release()
        # Release videowriter after the loop
        video_output.release()
        # Destroy all the windows
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()