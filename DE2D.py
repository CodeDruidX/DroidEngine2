v = "2.0.1"
print(f"Droid 2d Engine v{v} - rebuild")


import numpy as np
import cv2
import pygame


def img_into_polygon(np_img: np.float32, np_polygon: np.float32):
    h, w, _ = np_img.shape
    bounds = np.array(
        [[0.0, 0.0], [w, 0.0], [w, h], [0.0, h]]
    )  # Изначальный квадрат изображения

    heights, widths = np_polygon.T
    max_h, max_w = max(heights), max(widths)

    perspective = cv2.getPerspectiveTransform(bounds, np_polygon)  # Матрица поворота
    img = cv2.warpPerspective(np_img, perspective, (max_h, max_w), flags=cv2.INTER_AREA)

    return pygame.image.frombuffer(
        img.tobytes(), img.shape[1::-1], "RGBA"
    ).convert_alpha()  # Конвертация в pygame пригодный формат


def view(camera, coords):

    system = coords - camera[0]

    angle = np.arctan2(system[0], system[1]) - camera[1]
    length = np.linalg.norm(system)

    return angle, length


def screen_transform(angle, length, height, screen_dist_pixels, w, h):

    x_k = np.tan(angle) * screen_dist_pixels
    vert_angle = height / length

    y_k = vert_angle * screen_dist_pixels

    w = w / 2 + x_k
    h1 = h / 2 - y_k
    h2 = h / 2 + y_k
    return angle, int(w), int(h1), int(h2)


def render(camera, point, hei, d=1000, w=1920, h=1080, fov=90):
    angle, l = view(camera, point)
    return screen_transform(angle, l, hei, d, w, h)


# camera=[[x,y],[vert_angle,horis_angle]]
camera = [np.array([0.0, 0.0]), 1]


from math import hypot, sin, cos, atan, degrees, radians
import pygame
import pyautogui

WIDTH, HEIGHT = pyautogui.size()




import serial
SERIAL_RATE = 9600
SERIAL_PORT = 'COM8'
ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
global DIST
DIST=0
def updatedist():
    global DIST
    while ser.inWaiting():
        l=ser.readline().decode()
        DIST=int(l.strip())





pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
successes, failures = pygame.init()
pygame.event.set_allowed([pygame.QUIT])


screen = pygame.display.set_mode(
    (WIDTH, HEIGHT), flags=pygame.FULLSCREEN | pygame.DOUBLEBUF
)
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
FPS = 60  # Frames per second.

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# RED = (255, 0, 0), GREEN = (0, 255, 0), BLUE = (0, 0, 255).

myfont = pygame.font.SysFont("impact", 12)

logs = ""

speed = 0.01
pix_per_cm = 3678 / 100


while True:
    clock.tick(FPS)
    logs = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[pygame.K_w]:
        camera[0][0] += np.sin(camera[1]) * speed
        camera[0][1] += np.cos(camera[1]) * speed
    elif pressed_keys[pygame.K_s]:
        camera[0][0] += np.sin(camera[1] + np.pi) * speed
        camera[0][1] += np.cos(camera[1] + np.pi) * speed

    if pressed_keys[pygame.K_a]:
        camera[0][0] += np.sin(camera[1] - np.pi / 2) * speed
        camera[0][1] += np.cos(camera[1] - np.pi / 2) * speed
    elif pressed_keys[pygame.K_d]:
        camera[0][0] += np.sin(camera[1] + np.pi / 2) * speed
        camera[0][1] += np.cos(camera[1] + np.pi / 2) * speed

    if pressed_keys[pygame.K_q]:
        d += 1
    elif pressed_keys[pygame.K_e]:
        d -= 1

    if pressed_keys[pygame.K_LSHIFT]:
        speed += 0.001
    else:
        speed = max(0.01, speed - 0.003)

    if pressed_keys[pygame.K_o]:
        quit()

    x, y = pygame.mouse.get_pos()
    x -= WIDTH / 2

    pyautogui.moveTo(WIDTH / 2, HEIGHT / 2)
    camera[1] += x / 1000
    if camera[1] > np.pi:
        camera[1] -= np.pi * 2
    if camera[1] < -np.pi:
        camera[1] += np.pi * 2
    screen.fill(BLACK)

    updatedist()
    for i, ii in zip(range(1, 9), range(1, 9)):
        angle, x, y1, y2 = render(camera, np.float32([i, ii]), 0.6, d=DIST*pix_per_cm)
        if (
            (angle < np.radians(90) and angle > -np.radians(90))
            or (angle > (np.pi * 2 - np.pi / 2) and angle < np.pi * 2)
            or (angle < -(np.pi * 2 - np.pi / 2) and angle > -np.pi * 2)
        ):

            pygame.draw.circle(screen, WHITE, (x, y1), 10)
            pygame.draw.circle(screen, WHITE, (x, y2), 10)
            
    pygame.display.update()
