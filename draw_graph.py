import pygame, math

MULTIPLYER = 150
CIRCLE_SIZES = 30
COLOR = 'blue'

def main_draw(all_graphs):
    BASIC_SIZE = 500
    SIZE = (len(all_graphs) * BASIC_SIZE, 500)
    pygame.init()
    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    small_font = pygame.font.SysFont('Comic Sans MS', 20)
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    running = True
    screen.fill("white")
    pygame.display.set_caption('EULER AND HAMILTON GRAPHS')
    pygame.display.set_icon(pygame.image.load('./src/icon.png'))
    for ps_i, points in enumerate(all_graphs):
        connections_count = 0
        for i in range(len(points)):
            points[i].positionX = ps_i * BASIC_SIZE + (BASIC_SIZE / 2) + int(math.cos(i * 2*math.pi / len(points)) * MULTIPLYER)
            points[i].positionY = SIZE[1] / 2 + int(math.sin(i * 2*math.pi / len(points)) * MULTIPLYER)
        for i in range(len(points)):
            for connection in points[i].connections:
                    pygame.draw.line(screen, COLOR, (points[i].positionX, points[i].positionY), (connection.positionX, connection.positionY))
                    connections_count += 1
        for i in range(len(points)):
            pygame.draw.circle(screen, 'white', (points[i].positionX, points[i].positionY), CIRCLE_SIZES - 2, 100)
        for i in range(len(points)):
            text = my_font.render(points[i].name, False, COLOR)
            pygame.draw.circle(screen, COLOR, (points[i].positionX, points[i].positionY), CIRCLE_SIZES, 2)
            screen.blit(text, (points[i].positionX - CIRCLE_SIZES / 3, points[i].positionY - CIRCLE_SIZES / 1.5))
        text = small_font.render(f'CONNECTIONS {round((connections_count / (2 * (len(points) * (len(points) - 1) / 2))) * 100, 0)} %', False, COLOR)
        screen.blit(text, (ps_i * BASIC_SIZE + BASIC_SIZE / 2 - 100, 50))
            
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()