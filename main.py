import pygame
import random
from dot import Dot

def calculate_sq_distance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return dx**2 + dy**2


pygame.init()

WHITE=(255,255,255)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
MERGE = 10
START_NUM_DOTS = 10
MIN_DOTS = 10
MAX_DIST = 500
MAX_DIST_SQ = MAX_DIST**2
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Network Art")
alpha_surfaces = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

clock = pygame.time.Clock()
running = True

#List comprehension
dots = [Dot(SCREEN_WIDTH, SCREEN_HEIGHT, 
    random.randint(MERGE, SCREEN_WIDTH-MERGE), random.randint(MERGE, SCREEN_HEIGHT-MERGE))
    for _ in range(START_NUM_DOTS)]


while running: #True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #MOUSEBUTTONUP/MOUSEBUTTONDOWN
            x_click, y_click = event.pos
            dots.append(Dot(SCREEN_WIDTH, SCREEN_HEIGHT,
                x_click, y_click))
            

    """Блок отрисовки"""
    screen.fill((0, 0, 0)) #Fill black
    #Отрисовка точек
    for dot in dots:
        dot.move()
        # pygame.draw.line(screen, (50,50,50), (dot.x, dot.y), (dot.target_x, dot.target_y), 2)
        pygame.draw.circle(screen, WHITE, (dot.x, dot.y), 2)


    #Отрисовка линий
    alpha_surfaces.fill((0, 0, 0, 0))
    for i in range(len(dots)):
        for j in range(i+1, len(dots)):
            dot_A,dot_B = dots[i], dots[j]
            sq_distance = calculate_sq_distance(dot_A.x, dot_A.y, dot_B.x, dot_B.y)
            if sq_distance < MAX_DIST_SQ:
                closeness_factor = 1.0 - (sq_distance / MAX_DIST_SQ)
                brightness = int(closeness_factor * 255)
                pygame.draw.line(alpha_surfaces, (255, 255, 255, brightness),
                    (dot_A.x, dot_A.y), (dot_B.x, dot_B.y), 1)


    screen.blit(alpha_surfaces, (0, 0))

    #Фильтрация списка dots
    dots = [dot for dot in dots if not dot.is_at_target()]
    #Автоматическое добавление новых точек
    if len(dots) < MIN_DOTS:
        dots.append(Dot(SCREEN_WIDTH, SCREEN_HEIGHT))

    # print(len(dots))
    pygame.display.flip() #Update display
    clock.tick(FPS)
    # break
    # break

pygame.quit()