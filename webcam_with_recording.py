# Work for Sandberg webcamera
# import the opencv library
import cv2
import pygame
import time
import datetime


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

# Инициализация Pygame
pygame.init()
clock = pygame.time.Clock()

prev_time = time.time()
fps_counter = 0
real_fps = 10

# https://www.96boards.org/blog/rb3-1080p-opencv/
# define a video capture object
# cap = cv2.VideoCapture(0)
# codec = cv2.VideoWriter_fourcc(	'M', 'J', 'P', 'G'	)
# cap.set(6, codec)
# cap.set(5, 30)
# cap.set(3, 1920)
# cap.set(4, 1080)

##############################################################
########################## GSTREAMER ########################
# https://gstreamer.freedesktop.org/download/#windows
# https://stackoverflow.com/questions/17278953/gstreamer-python-bindings-for-windows
# https://www.programcreek.com/python/example/110718/cv2.CAP_GSTREAMER
# https://programtalk.com/python-more-examples/cv2.CAP_GSTREAMER/?utm_content=cmp-true
# cap = cv2.VideoCapture("v4l2src device=/dev/video0 ! image/jpeg,framerate=30/1,width=1920, height=1080,type=video ! jpegdec ! videoconvert ! video/x-raw ! appsink", cv2.CAP_GSTREAMER)
# cap = cv2.VideoCapture("v4l2src ! videoscale ! video/x-raw, width=1920, height=1080 ! videoconvert ! appsink", cv2.CAP_GSTREAMER)
# cap = cv2.VideoCapture("videotestsrc ! video/x-raw,width=1920,heigh=1080 ! videoconvert ! video/x-raw ! appsink", cv2.CAP_GSTREAMER)
##############################################################
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# fps = 10.0
fourcc = cv2.VideoWriter.fourcc('M', 'J', 'P', 'G')
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Work as ('M', 'J', 'P', 'G')
# fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # Not working
# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # Not working
# fourcc = -1  # Work but 640x480 for DroidCam
# fourcc = 0   # Not working
# fourcc = cv2.VideoWriter.fourcc('P', 'I', 'M', '1')  # Not working
# fourcc = cv2.VideoWriter_fourcc(*'avc1')  # Not working
# fourcc = cv2.VideoWriter_fourcc(*'X264')  # Not working
# fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Not working
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Not working
# fourcc = cv2.VideoWriter.fourcc('m', 'j', 'p', 'g') # Not working
# cap.set(cv2.CAP_PROP_FPS, fps)
cap.set(cv2.CAP_PROP_FOURCC, fourcc)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
# or
# width = cap.get(3)  # float `width`
# height = cap.get(4)  # float `height`

print(f'width x height: {width} x {height}')

# ============================== OUTPUT VIDEO ==================================
write_video = True
path_2_video_output = f'simple_video_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}.mp4'
fps_output = 30

# Инициализировать объект записи видео
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_output = cv2.VideoWriter(path_2_video_output, fourcc, fps_output, (width, height))
# ============================== OUTPUT VIDEO ==================================

fps = cap.get(cv2.CAP_PROP_FPS)
# or
# fps = cap.get(5)

print(f'fps from cap.get: {fps}')  # float `fps`

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
counter = 0
while True:

    # Capture the video frame
    # by frame
    ret, frame = cap.read()
    if ret:
        frame_with_center_lines = draw_center_lines(frame.copy(), width / 2, height / 2)
    counter += 1
    fps_counter += 1

    ############################################################################
    # Поворот изображения на 180 градусов
    # frame = cv2.flip(frame, -1)  # -1 означает поворот на 180 градусов
    ############################################################################

    # ============================== FPS =======================================
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f'fps from cap.get: {fps}')

    if time.time() - prev_time >= 1:
        elapsed_time = time.time() - prev_time
        real_fps = fps_counter / elapsed_time
        fps_counter = 0
        prev_time = time.time()

    print(f"Real FPS: {real_fps}")

    clock.tick()  # Счетчик времени для FPS

    # Получение текущего FPS
    pygame_fps = clock.get_fps()
    print(f"Current FPS: {pygame_fps:.2f}")
    # ============================== FPS =======================================

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print('frames count:', frame_count)  # float `frame_count`
    zoom = cap.get(cv2.CAP_PROP_ZOOM)
    print('zoom:', zoom)
    focus = cap.get(cv2.CAP_PROP_FOCUS)
    print('focus:', focus)
    autofocus = cap.get(cv2.CAP_PROP_AUTOFOCUS)
    print('autofocus:', autofocus)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice

    # Display the resulting frame
    cv2.imshow('frame', frame_with_center_lines)

    if write_video:
        video_output.write(frame)

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

# Release the cap object after the loop
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()
