import pygame
import sys
import os

# Инициализация
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90
BALL_SIZE = 15
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong with Mox Background")
clock = pygame.time.Clock()

# --- ЗАГРУЗКА ФОНА ---
# Пытаемся загрузить изображение
IMAGE_FILENAME = "mox.jpg"
background_image = IMAGE_FILENAME

if os.path.exists(IMAGE_FILENAME):
    try:
        # Загружаем
        original_bg = pygame.image.load(IMAGE_FILENAME)
        # Масштабируем под размер окна (800x600)
        background_image = pygame.transform.scale(original_bg, (WIDTH, HEIGHT))
    except pygame.error as e:
        print(f"Ошибка при загрузке изображения: {e}")
        print("Игра запустится с черным фоном.")
else:
    print(f"Файл {IMAGE_FILENAME} не найден в папке со скриптом.")
    print("Игра запустится с черным фоном.")
# ---------------------

# Объекты (прямоугольники Rect)
paddle_a = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_b = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Скорости
ball_speed_x = 5
ball_speed_y = 5
paddle_speed = 7

# Счет
score_a = 0
score_b = 0
# Используем жирный шрифт для лучшей читаемости на фоне
font = pygame.font.SysFont("Arial", 40, bold=True)

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH//2, HEIGHT//2)
    # При сбросе немного меняем угол, чтобы не было скучно
    ball_speed_x *= -1

# Основной цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle_a.top > 0:
        paddle_a.y -= paddle_speed
    if keys[pygame.K_s] and paddle_a.bottom < HEIGHT:
        paddle_a.y += paddle_speed
    if keys[pygame.K_UP] and paddle_b.top > 0:
        paddle_b.y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle_b.bottom < HEIGHT:
        paddle_b.y += paddle_speed

    # Движение мяча
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Отскоки от стен (верх/низ)
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Проверка гола
    if ball.left <= 0:
        score_b += 1
        reset_ball()
    if ball.right >= WIDTH:
        score_a += 1
        reset_ball()

    # Столкновение с ракетками
    if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
        ball_speed_x *= -1
        # Немного ускоряем мяч при ударе, чтобы игра была динамичнее
        ball_speed_x *= 1.02
        ball_speed_y *= 1.02

    # Отрисовка
    # 1. Сначала рисуем фон
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(BLACK) # Если картинки нет, заливаем черным

    # 2. Рисуем полупрозрачную разделительную линию
    # Создаем временную поверхность для линии
    line_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.aaline(line_surf, (255, 255, 255, 128), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    screen.blit(line_surf, (0,0))

    # 3. Рисуем игровые объекты
    pygame.draw.rect(screen, WHITE, paddle_a)
    pygame.draw.rect(screen, WHITE, paddle_b)
    pygame.draw.ellipse(screen, WHITE, ball)

    # 4. Рисуем текст счета (добавляем небольшую тень для читаемости)
    score_str = f"{score_a}   {score_b}"
    
    # Тень (черная)
    score_text_shadow = font.render(score_str, True, BLACK)
    shadow_pos = (WIDTH // 2 - score_text_shadow.get_width() // 2 + 2, 22)
    screen.blit(score_text_shadow, shadow_pos)
    
    # Основной текст (белый)
    score_text = font.render(score_str, True, WHITE)
    text_pos = (WIDTH // 2 - score_text.get_width() // 2, 20)
    screen.blit(score_text, text_pos)

    pygame.display.flip()
    clock.tick(FPS)