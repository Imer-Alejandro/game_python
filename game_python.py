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

def get_game_state():
    state = {
        'A': elements.get('A', [])[0] if 'A' in elements else None,
        'goal': elements.get('0', [])[0] if '0' in elements else None,
        'obstacles': {k: v[:] for k, v in elements.items() if k not in ('A', '0')}
    }
    return state

# Leer el nivel desde el archivo txt
rows, cols = read_level_from_txt('nivel.txt')

# Ejemplo de movimiento para actualizar el estado
# Simula que el jugador 'A' se mueve hacia la derecha
def move_player_right():
    if 'A' in elements:
        current_pos = elements['A'][0]
        new_pos = (current_pos[0] + 1, current_pos[1])
        elements['A'] = [new_pos]

# Ejemplo de actualización del estado después de mover al jugador
game_state = get_game_state()
print("Estado actualizado del juego:", game_state)

# Aquí puedes pasar game_state a tus algoritmos de búsqueda para que puedan trabajar con el estado dinámico del juego.

# Bucle principal del juego (solo dibujo, no afecta al estado)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, BLACK, rect, 1)

    for letter, positions in elements.items():
        if letter == 'A':
            color = RED
        elif letter == '0':
            color = GREEN
        elif letter == 'B':
            color = GRAY  # Color gris para obstáculos de una sola letra
        else:
            color = BLUE
        
        for pos in positions:
            x, y = pos
            orientation = determine_orientation(positions)
            if len(letter) == 1:
                # Para elementos de una sola letra, ocupan solo una casilla
                element_rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            elif orientation == 'vertical':
                element_rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size * len(positions))
            elif orientation == 'horizontal':
                element_rect = pygame.Rect(x * cell_size, y * cell_size, cell_size * len(positions), cell_size)
            else:
                continue
            
            pygame.draw.rect(screen, color, element_rect)
            font = pygame.font.Font(None, 36)
            text = font.render(letter, True, WHITE)
            screen.blit(text, (element_rect.x + 10, element_rect.y + 5))

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
sys.exit()
