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
selected_element = None

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

def is_position_free(x, y, exclude_letter=None):
    for letter, positions in elements.items():
        if letter != exclude_letter:
            if (x, y) in positions:
                return False
    return True

def move_element(letter, key):
    if letter not in elements:
        return False
    
    positions = elements[letter]
    orientation = determine_orientation(positions)
    new_positions = []

    for x, y in positions:
        if orientation == 'vertical':
            if key == pygame.K_UP:
                new_pos = (x, y - 1)
            elif key == pygame.K_DOWN:
                new_pos = (x, y + 1)
        elif orientation == 'horizontal':
            if key == pygame.K_LEFT:
                new_pos = (x - 1, y)
            elif key == pygame.K_RIGHT:
                new_pos = (x + 1, y)
        else:
            continue
        
        if new_pos[0] < 0 or new_pos[0] >= cols or new_pos[1] < 0 or new_pos[1] >= rows:
            return False  # Movimiento fuera de los límites del tablero
        if not is_position_free(*new_pos, exclude_letter=letter):
            return False  # Posición ocupada por otro elemento
        
        new_positions.append(new_pos)

    if len(new_positions) == len(positions):
        elements[letter] = new_positions
        return True
    return False

# Leer el nivel desde el archivo txt
rows, cols = read_level_from_txt('nivel.txt')

# Ejemplo de actualización del estado después de mover al jugador
game_state = get_game_state()
print("Estado actualizado del juego:", game_state)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.unicode in elements:
                selected_element = event.unicode
                print(f"Elemento '{selected_element}' seleccionado")
            elif selected_element:
                if move_element(selected_element, event.key):
                    print(f"Elemento '{selected_element}' movido con éxito")
                else:
                    print(f"No se puede mover el elemento '{selected_element}' en esa dirección")

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