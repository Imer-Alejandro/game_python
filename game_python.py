import pygame
import sys

pygame.init()

# Parámetros de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Juego de Tablero')

# Variables de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)  # Color gris

# Tamaño de cada celda
cell_size = 50

# Diccionario para almacenar elementos del tablero y sus propiedades
elements = {}

def read_level_from_txt(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    rows = len(lines)
    cols = len(lines[0].strip())
    elements.clear()

    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if char == '.':
                continue
            create_element(char, x, y)

    return rows, cols

def create_element(letter, x, y):
    if letter not in elements:
        elements[letter] = []
    elements[letter].append((x, y))

def determine_orientation(element):
    positions = element
    if len(positions) == 1:
        return 'obstacle'
    elif len(set(x for x, y in positions)) == 1:
        return 'vertical'
    else:
        return 'horizontal'

def draw_board(rows, cols):
    screen.fill(WHITE)
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, BLACK, rect, 1)

def draw_elements():
    for letter, positions in elements.items():
        if letter == 'X':
            color = RED
        elif letter == '0':
            color = GREEN
        elif len(letter) == 1:
            color = BLUE  # Color gris para obstáculos de una sola letra
        else:
            color = BLUE
        
        for pos in positions:
            x, y = pos
            orientation = determine_orientation(positions)
            if len(letter) == 1:
                # Para elementos de una sola letra, ocupan solo una casilla
                element_rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            elif orientation == 'vertical':
                element_rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size * len(letter))
            elif orientation == 'horizontal':
                element_rect = pygame.Rect(x * cell_size, y * cell_size, cell_size * len(letter), cell_size)
            else:
                continue
            
            pygame.draw.rect(screen, color, element_rect)
            font = pygame.font.Font(None, 36)
            text = font.render(letter, True, WHITE)
            screen.blit(text, (element_rect.x + 10, element_rect.y + 5))

# Leer el nivel desde el archivo txt
rows, cols = read_level_from_txt('nivel.txt')

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_board(rows, cols)
    draw_elements()
    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
sys.exit()